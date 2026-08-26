#!/usr/bin/env python3
"""
osint_regex_scan.py
====================

Scanner de expressões regulares baseado no dataset público
`osint-brazuca-regex` (https://github.com/osintbrazuca/osint-brazuca-regex).

Recursos:
  - Lê o banco de regex a partir do JSON oficial do repositório
    (63 categorias / 346 padrões: CPF, CNPJ, e-mail, telefone, cartão de
    crédito, chaves de wallet cripto, chave PIX, tokens de API, IPv4/IPv6,
    domínios .br, .onion, dados bancários, etc).
  - Entrada via stdin (pipe), arquivo único ou pasta (recursiva).
  - Filtragem por categoria de regex (--categories / --exclude-categories).
  - Descrição do achado em modo "short" (chave da categoria) ou "long"
    (descrição completa do JSON), ou "both".
  - Saída em terminal (colorida), "normal" (texto plano tabulado),
    csv ou json.
  - Escaneamento multi-thread de pastas (ThreadPoolExecutor).
  - Leitura de arquivos grandes via mmap + streaming linha a linha, para
    não carregar o arquivo inteiro na memória; e opção de tentar
    aumentar o limite de memória do processo (RLIMIT_AS) em Linux/macOS.
  - Detecção de tipo por assinatura (não por extensão): só casa regex sobre
    TEXTO. Documentos (PDF, DOCX, XLSX, PPTX, ODT/ODS/ODP, EPUB, RTF) têm o
    texto extraído antes do casamento; demais binários são pulados.
  - Filtro de ruído textual: linhas gigantes sem espaço e blobs base64/hex
    (imagem embutida em SVG, anexo de .eml, JS minificado) não geram achado.

Exemplos:
  python osint_regex_scan.py --list-categories

  python osint_regex_scan.py arquivo.txt --categories cpf,email

  python osint_regex_scan.py ./dump --categories cnpj,email,creditCard \\
      --format csv --out achados.csv --threads 16

  cat vazamento.log | python osint_regex_scan.py --format json --desc short

  grep -R "senha" /var/log | python osint_regex_scan.py --categories email,cpf
"""
from __future__ import annotations

import argparse
import codecs
import collections
import csv
import html
import io
import json
import mmap
import os
import re
import shutil
import subprocess
import sys
import time
import zipfile
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Iterable, Iterator, Optional

try:
    import resource  # POSIX apenas (Linux/macOS)
except ImportError:  # pragma: no cover - Windows
    resource = None

try:
    import chardet  # opcional: melhora a detecção de encoding quando presente
except ImportError:
    chardet = None

SCRIPT_DIR = Path(__file__).resolve().parent
DATASET_DIR = SCRIPT_DIR / "dataset"
# O dataset é editado em dois arquivos, por contexto. O osint-brazuca-regex.json
# unificado ainda existe (legado, gerado por dataset/build.py), mas o padrão da
# ferramenta é carregar os dois (ver --scope).
DB_POR_ESCOPO = {
    "br": DATASET_DIR / "osint-brazuca-regex-br.json",
    "geral": DATASET_DIR / "osint-brazuca-regex-geral.json",
}
DEFAULT_JSON_PATHS = [DB_POR_ESCOPO["geral"], DB_POR_ESCOPO["br"]]


# --------------------------------------------------------------------------- #
# Cores no terminal
# --------------------------------------------------------------------------- #
class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    GRAY = "\033[90m"


def colorize(text: str, code: str, enabled: bool) -> str:
    return f"{code}{text}{Color.RESET}" if enabled else text


# --------------------------------------------------------------------------- #
# Estruturas de dados
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class RegexRule:
    category: str
    index: int
    description: str
    raw_pattern: str
    pattern: "re.Pattern[str]"
    scope: str = ""      # "br" | "geral": de qual arquivo do dataset a regra veio


@dataclass
class Match:
    source: str
    line: int
    col: int
    category: str
    description: str
    value: str
    scope: str = ""


# --------------------------------------------------------------------------- #
# Normalização dos padrões do JSON
#
# O dataset foi escrito pensando em JS/PCRE. Duas situações não são
# compatíveis com o módulo `re` do Python e precisam de tratamento:
#   1) Padrões delimitados no estilo JS: "/padrao/flags" (ex.: categoria
#      "correios").
#   2) Flags inline "(?i)" que não estão no início do padrão, que o Python
#      3.11+ rejeita isso com "global flags not at the start of the
#      expression" (ex.: categoria "crm"). Nesses casos extraímos a flag
#      e aplicamos globalmente via re.compile(pattern, flags).
# --------------------------------------------------------------------------- #
FLAG_MAP = {
    "i": re.IGNORECASE,
    "m": re.MULTILINE,
    "s": re.DOTALL,
    "x": re.VERBOSE,
    "a": re.ASCII,
    "u": 0,
    "g": 0,  # "global" no JS; no Python finditer já retorna todas as ocorrências
}

JS_DELIM_RE = re.compile(r"^/(.*)/([a-zA-Z]*)$", re.DOTALL)
INLINE_FLAG_RE = re.compile(r"\(\?([aiLmsux]+)\)")


def normalize_pattern(raw: str) -> tuple[str, int]:
    """Converte um padrão do JSON para algo compilável pelo módulo `re`."""
    flags = 0
    pattern = raw

    m = JS_DELIM_RE.match(raw)
    if m:
        pattern, flagstr = m.group(1), m.group(2)
        for ch in flagstr:
            flags |= FLAG_MAP.get(ch.lower(), 0)

    new_pattern = pattern
    offset = 0
    for mm in INLINE_FLAG_RE.finditer(pattern):
        if mm.start() == 0:
            continue  # flag global no início é válida em Python
        for ch in mm.group(1):
            flags |= FLAG_MAP.get(ch.lower(), 0)
        start, end = mm.start() - offset, mm.end() - offset
        new_pattern = new_pattern[:start] + new_pattern[end:]
        offset += mm.end() - mm.start()

    return new_pattern, flags


# --------------------------------------------------------------------------- #
# Carregamento do banco de regex
# --------------------------------------------------------------------------- #
def resolver_dbs(caminhos: "list[str] | None", scope: str = "todos") -> list[Path]:
    """
    Resolve os caminhos do banco de regex. Aceita arquivos avulsos ou uma pasta
    (nesse caso, todos os *.json dela, exceto o unificado legado, que duplicaria
    o conteúdo dos dois arquivos por contexto).
    """
    if not caminhos:
        if scope in DB_POR_ESCOPO:
            return [DB_POR_ESCOPO[scope]]
        return list(DEFAULT_JSON_PATHS)

    resolvidos: list[Path] = []
    for bruto in caminhos:
        p = Path(bruto)
        if p.is_dir():
            for f in sorted(p.glob("*.json")):
                if f.name == "osint-brazuca-regex.json" and len(list(p.glob("*.json"))) > 1:
                    continue  # unificado é artefato gerado: pular para não duplicar
                resolvidos.append(f)
        else:
            resolvidos.append(p)

    if scope in DB_POR_ESCOPO:
        alvo = DB_POR_ESCOPO[scope].name
        filtrados = [f for f in resolvidos if f.name == alvo]
        if filtrados:
            return filtrados
    return resolvidos


def escopo_do_arquivo(path: Path) -> str:
    for escopo, alvo in DB_POR_ESCOPO.items():
        if path.name == alvo.name:
            return escopo
    return ""


def load_raw_db(json_paths: "Path | list[Path]") -> "collections.OrderedDict[str, list]":
    """
    Carrega um ou mais arquivos do dataset, MESCLANDO as categorias.

    A mescla é essencial: creditCard, socialMedia, apiCredentials e vehicles
    existem nos dois arquivos (a parte brasileira num, a geral no outro).
    Um dict.update() simples faria o segundo arquivo sobrescrever o primeiro
    e perder metade das regras.
    """
    if isinstance(json_paths, Path):
        json_paths = [json_paths]

    combinado: "collections.OrderedDict[str, list]" = collections.OrderedDict()
    for path in json_paths:
        with path.open(encoding="utf-8") as f:
            raw = json.load(f, object_pairs_hook=collections.OrderedDict)
        escopo = escopo_do_arquivo(path)
        for categoria, entradas in raw.items():
            marcadas = [dict(e, _scope=escopo) for e in entradas]
            combinado.setdefault(categoria, []).extend(marcadas)
    return combinado


def load_rules(
    json_paths: "Path | list[Path]",
    include: Optional[set[str]] = None,
    exclude: Optional[set[str]] = None,
) -> tuple[list[RegexRule], list[tuple[str, int, str, str]]]:
    raw = load_raw_db(json_paths)

    if include:
        unknown = include - set(raw.keys())
        if unknown:
            print(
                f"[!] categorias desconhecidas ignoradas: {', '.join(sorted(unknown))}",
                file=sys.stderr,
            )

    rules: list[RegexRule] = []
    errors: list[tuple[str, int, str, str]] = []

    for cat, entries in raw.items():
        if include and cat not in include:
            continue
        if exclude and cat in exclude:
            continue
        for idx, entry in enumerate(entries):
            raw_pattern = entry.get("regex", "")
            desc = entry.get("description", "")
            pattern_src, flags = normalize_pattern(raw_pattern)
            try:
                compiled = re.compile(pattern_src, flags)
            except re.error as e:
                errors.append((cat, idx, raw_pattern, str(e)))
                continue
            rules.append(
                RegexRule(
                    category=cat,
                    index=idx,
                    description=desc,
                    raw_pattern=raw_pattern,
                    pattern=compiled,
                    scope=entry.get("_scope", ""),
                )
            )
    return rules, errors


def print_categories(json_paths: "Path | list[Path]") -> None:
    raw = load_raw_db(json_paths)
    print(f"{'categoria':30} {'escopo':>12} {'qtd':>4}  exemplo de descrição")
    print("-" * 110)
    por_escopo: "collections.Counter[str]" = collections.Counter()
    for cat in sorted(raw.keys()):
        entries = raw[cat]
        escopos = sorted({e.get("_scope", "") for e in entries} - {""})
        for e in entries:
            por_escopo[e.get("_scope", "?")] += 1
        rotulo = "+".join(escopos) if escopos else "?"
        example = entries[0]["description"] if entries else ""
        print(f"{cat:30} {rotulo:>12} {len(entries):>4}  {example[:52]}")
    total = sum(len(v) for v in raw.values())
    detalhe = ", ".join(f"{k}: {v}" for k, v in sorted(por_escopo.items()))
    print(f"\nTotal: {len(raw)} categorias, {total} padrões de regex." + (f"  ({detalhe})" if detalhe else ""))


# --------------------------------------------------------------------------- #
# Detecção de tipo de conteúdo
#
# Regex só faz sentido sobre texto. Escanear os bytes crus de um documento
# produz falso positivo em massa: um PDF de 66 KB rende milhares de "CPFs" e
# "cartões" que na verdade são offsets, streams comprimidos e timestamps.
#
# A detecção antiga procurava um byte NUL nos primeiros 1024 bytes. Isso não
# funciona para formatos com cabeçalho ASCII: um PDF começa com "%PDF-1.x" e
# objetos legíveis, e o primeiro NUL costuma cair bem além de 1 KB (ou nem
# existir, em PDFs sem stream comprimido). A classificação abaixo usa, nesta
# ordem: BOM -> assinatura (número mágico) -> NUL -> proporção de bytes de
# controle. Extensão de arquivo nunca é usada como critério.
# --------------------------------------------------------------------------- #
SNIFF_SIZE = 8192
NON_TEXT_RATIO = 0.30

KIND_TEXT = "text"
KIND_DOCUMENT = "document"
KIND_BINARY = "binary"

# Bytes de controle aceitáveis em texto (tab, LF, VT, FF, CR, ESC).
_CONTROL_OK = frozenset({0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x1B})

# Assinaturas no início do arquivo. Ordem importa: prefixos mais longos antes.
_SIGNATURES: tuple[tuple[bytes, str], ...] = (
    (b"%PDF-", "pdf"),
    (b"{\\rtf", "rtf"),
    (b"%!PS", "postscript"),
    (b"PK\x03\x04", "zip"),
    (b"PK\x05\x06", "zip"),
    (b"\x7fELF", "elf"),
    (b"\x89PNG\r\n\x1a\n", "png"),
    (b"\xff\xd8\xff", "jpeg"),
    (b"GIF87a", "gif"),
    (b"GIF89a", "gif"),
    (b"BM", "bmp"),
    (b"\x00\x00\x01\x00", "ico"),
    (b"RIFF", "riff"),
    (b"\x1f\x8b", "gzip"),
    (b"BZh", "bzip2"),
    (b"\xfd7zXZ\x00", "xz"),
    (b"\x04\x22\x4d\x18", "lz4"),
    (b"\x28\xb5\x2f\xfd", "zstd"),
    (b"7z\xbc\xaf\x27\x1c", "7z"),
    (b"Rar!\x1a\x07", "rar"),
    (b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1", "ole2"),
    (b"SQLite format 3\x00", "sqlite"),
    (b"\x00asm", "wasm"),
    (b"MZ", "pe"),
    (b"\xca\xfe\xba\xbe", "class"),
    (b"OggS", "ogg"),
    (b"fLaC", "flac"),
    (b"ID3", "mp3"),
    (b"wOFF", "woff"),
    (b"wOF2", "woff2"),
    (b"OTTO", "otf"),
    (b"\x00\x01\x00\x00\x00", "ttf"),
    (b"-----BEGIN ", "pem"),
)

# Formatos de container cujo texto sabemos extrair.
_DOCUMENT_FORMATS = frozenset({
    "pdf", "rtf", "docx", "xlsx", "pptx", "odt", "ods", "odp", "epub",
})

_BOMS: tuple[tuple[bytes, str], ...] = (
    (codecs.BOM_UTF8, "utf-8-sig"),
    (codecs.BOM_UTF32_LE, "utf-32"),
    (codecs.BOM_UTF32_BE, "utf-32"),
    (codecs.BOM_UTF16_LE, "utf-16"),
    (codecs.BOM_UTF16_BE, "utf-16"),
)


@dataclass(frozen=True)
class ContentInfo:
    kind: str        # KIND_TEXT | KIND_DOCUMENT | KIND_BINARY
    fmt: str         # "plain", "pdf", "docx", "png", ...
    encoding: str    # relevante quando kind == KIND_TEXT
    reason: str      # por que foi classificado assim (usado nos avisos)


def _non_text_ratio(data: bytes) -> float:
    """Proporção de bytes de controle não-textuais, no espírito do git/grep."""
    if not data:
        return 0.0
    bad = sum(1 for b in data if (b < 0x20 and b not in _CONTROL_OK) or b == 0x7F)
    return bad / len(data)


def detect_encoding(data: bytes) -> str:
    for bom, enc in _BOMS:
        if data.startswith(bom):
            return enc
    try:
        data.decode("utf-8")
        return "utf-8"
    except UnicodeDecodeError as e:
        # Um caractere multibyte cortado no fim do sniff não invalida o arquivo.
        if e.start >= len(data) - 4:
            return "utf-8"
    if chardet is not None:
        try:
            guess = chardet.detect(data)
            if guess and guess.get("encoding") and (guess.get("confidence") or 0) >= 0.8:
                return guess["encoding"]
        except Exception:  # pragma: no cover - chardet é opcional e best-effort
            pass
    return "latin-1"


def _zip_subtype(source: "Path | bytes") -> tuple[str, str]:
    """Distingue DOCX/XLSX/PPTX/ODF/EPUB de um ZIP comum, olhando o conteúdo."""
    try:
        handle = io.BytesIO(source) if isinstance(source, bytes) else source
        with zipfile.ZipFile(handle) as zf:
            names = set(zf.namelist())
            if "mimetype" in names:
                try:
                    mime = zf.read("mimetype").decode("ascii", "replace").strip()
                except Exception:
                    mime = ""
                for suffix, fmt in (("opendocument.text", "odt"),
                                    ("opendocument.spreadsheet", "ods"),
                                    ("opendocument.presentation", "odp"),
                                    ("epub+zip", "epub")):
                    if mime.endswith(suffix):
                        return fmt, f"zip com mimetype {mime}"
            if "word/document.xml" in names:
                return "docx", "zip com word/document.xml"
            if "xl/workbook.xml" in names:
                return "xlsx", "zip com xl/workbook.xml"
            if "ppt/presentation.xml" in names:
                return "pptx", "zip com ppt/presentation.xml"
            if "META-INF/container.xml" in names:
                return "epub", "zip com META-INF/container.xml"
    except (zipfile.BadZipFile, OSError, ValueError):
        pass
    return "zip", "arquivo ZIP sem parte de texto conhecida"


def detect_content(data: bytes, source: "Path | None" = None) -> ContentInfo:
    """Classifica um conteúdo a partir do seu início (sniff)."""
    if not data:
        return ContentInfo(KIND_TEXT, "plain", "utf-8", "arquivo vazio")

    for bom, enc in _BOMS:
        if data.startswith(bom):
            return ContentInfo(KIND_TEXT, "plain", enc, f"BOM {enc}")

    for sig, fmt in _SIGNATURES:
        if data.startswith(sig):
            if fmt == "zip":
                fmt, reason = _zip_subtype(source if source is not None else data)
            else:
                reason = f"assinatura de {fmt}"
            if fmt in _DOCUMENT_FORMATS:
                return ContentInfo(KIND_DOCUMENT, fmt, "utf-8", reason)
            if fmt in ("postscript", "pem"):
                return ContentInfo(KIND_TEXT, "plain", detect_encoding(data), reason)
            return ContentInfo(KIND_BINARY, fmt, "", reason)

    if b"\x00" in data:
        return ContentInfo(KIND_BINARY, "unknown", "", f"byte NUL no offset {data.find(b'\\x00')}")

    ratio = _non_text_ratio(data)
    if ratio > NON_TEXT_RATIO:
        return ContentInfo(KIND_BINARY, "unknown", "", f"{ratio:.0%} de bytes de controle")

    return ContentInfo(KIND_TEXT, "plain", detect_encoding(data), "conteúdo textual")


def sniff_path(path: Path) -> ContentInfo:
    try:
        with path.open("rb") as f:
            head = f.read(SNIFF_SIZE)
    except OSError as e:
        return ContentInfo(KIND_BINARY, "unknown", "", f"erro de leitura: {e}")
    return detect_content(head, path)


def looks_binary(path: Path, sniff: int = SNIFF_SIZE) -> bool:
    """Compatibilidade: True quando o arquivo não é texto puro."""
    return sniff_path(path).kind != KIND_TEXT


# --------------------------------------------------------------------------- #
# Extratores de texto
#
# Contrato: recebe o caminho (ou os bytes, no caso do stdin) e devolve o texto
# do documento, ou None quando não há como extrair neste ambiente. Formatos
# baseados em ZIP+XML e RTF usam só a biblioteca padrão. PDF tenta, em ordem,
# o binário `pdftotext` (poppler) e depois pypdf/PyPDF2. Se nenhum existir, o
# arquivo é pulado com aviso, nunca escaneado cru.
# --------------------------------------------------------------------------- #
PDFTOTEXT_TIMEOUT = 120

# Fecha parágrafo/célula nos formatos XML: sem isso o documento inteiro vira
# uma única linha gigante e o número de linha do achado perde o sentido.
_XML_BREAKS = re.compile(
    rb"</(?:w:p|a:p|text:p|text:h|si|row|c|tr|p|div|br|li|h[1-6])\s*>|<(?:w:br|a:br|text:line-break|br)\s*/>",
)

_ZIP_PARTS: dict[str, tuple[str, ...]] = {
    "docx": ("word/document.xml", "word/footnotes.xml", "word/endnotes.xml", "word/comments.xml"),
    "xlsx": ("xl/sharedStrings.xml",),
    "pptx": (),
    "odt": ("content.xml", "styles.xml"),
    "ods": ("content.xml",),
    "odp": ("content.xml",),
    "epub": (),
}

_ZIP_GLOBS: dict[str, tuple[str, ...]] = {
    "docx": ("word/header", "word/footer"),
    "xlsx": ("xl/worksheets/sheet",),
    "pptx": ("ppt/slides/slide", "ppt/notesSlides/notesSlide"),
    "epub": (".xhtml", ".html", ".htm"),
}


def _xml_to_text(blob: bytes) -> str:
    blob = _XML_BREAKS.sub(lambda m: m.group(0) + b"\n", blob)
    try:
        root = ET.fromstring(blob)
    except ET.ParseError:
        # Fallback tolerante: remove as tags na marra.
        return html.unescape(re.sub(rb"<[^>]+>", b" ", blob).decode("utf-8", "replace"))
    return "".join(root.itertext())


def extract_zip_document(path: "Path | bytes", fmt: str) -> Optional[str]:
    partes: list[str] = []
    try:
        handle = io.BytesIO(path) if isinstance(path, bytes) else path
        with zipfile.ZipFile(handle) as zf:
            nomes = zf.namelist()
            alvos = [n for n in _ZIP_PARTS.get(fmt, ()) if n in nomes]
            for prefixo in _ZIP_GLOBS.get(fmt, ()):
                alvos += sorted(
                    n for n in nomes
                    if (n.startswith(prefixo) or n.endswith(prefixo)) and n not in alvos
                )
            for nome in alvos:
                try:
                    partes.append(_xml_to_text(zf.read(nome)))
                except (KeyError, zipfile.BadZipFile, OSError):
                    continue
    except (zipfile.BadZipFile, OSError, ValueError):
        return None
    texto = "\n".join(p for p in partes if p.strip())
    return texto or None


_RTF_DESTINOS = re.compile(
    r"\{\\\*?\\(?:fonttbl|colortbl|stylesheet|info|pict|object|themedata|datastore|latentstyles)[^{}]*"
    r"(?:\{[^{}]*\}[^{}]*)*\}",
    re.DOTALL,
)
_RTF_HEX = re.compile(r"\\'([0-9a-fA-F]{2})")
_RTF_QUEBRA = re.compile(r"\\(?:par|line|page|sect)\b")
_RTF_CONTROLE = re.compile(r"\\[a-zA-Z]+-?\d*\s?")


def extract_rtf(data: bytes) -> Optional[str]:
    texto = data.decode("latin-1", "replace")
    anterior = None
    while anterior != texto:  # grupos de destino podem estar aninhados
        anterior = texto
        texto = _RTF_DESTINOS.sub(" ", texto)
    texto = _RTF_QUEBRA.sub("\n", texto)
    texto = _RTF_HEX.sub(lambda m: bytes([int(m.group(1), 16)]).decode("latin-1"), texto)
    texto = _RTF_CONTROLE.sub(" ", texto)
    texto = texto.replace("\\{", "{").replace("\\}", "}").replace("\\\\", "\\")
    texto = re.sub(r"[{}]", " ", texto)
    return texto or None


def _pdf_via_pdftotext(source: "Path | bytes") -> Optional[str]:
    exe = shutil.which("pdftotext")
    if not exe:
        return None
    try:
        if isinstance(source, bytes):
            proc = subprocess.run([exe, "-q", "-layout", "-", "-"], input=source,
                                  capture_output=True, timeout=PDFTOTEXT_TIMEOUT)
        else:
            proc = subprocess.run([exe, "-q", "-layout", str(source), "-"],
                                  capture_output=True, timeout=PDFTOTEXT_TIMEOUT)
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode != 0 and not proc.stdout:
        return None
    return proc.stdout.decode("utf-8", "replace") or None


def _pdf_via_pypdf(source: "Path | bytes") -> Optional[str]:
    reader_cls = None
    for modname in ("pypdf", "PyPDF2"):
        try:
            reader_cls = __import__(modname).PdfReader
            break
        except (ImportError, AttributeError):
            continue
    if reader_cls is None:
        return None
    try:
        alvo = io.BytesIO(source) if isinstance(source, bytes) else str(source)
        reader = reader_cls(alvo)
        paginas = [(p.extract_text() or "") for p in reader.pages]
    except Exception:  # a biblioteca levanta exceções próprias e variadas
        return None
    texto = "\n".join(paginas)
    return texto or None


def extract_pdf(source: "Path | bytes") -> tuple[Optional[str], str]:
    """Devolve (texto, nome_do_extrator). texto None = nenhum extrator disponível."""
    texto = _pdf_via_pdftotext(source)
    if texto is not None:
        return texto, "pdftotext"
    texto = _pdf_via_pypdf(source)
    if texto is not None:
        return texto, "pypdf"
    return None, ""


def pdf_extractors_disponiveis() -> list[str]:
    disponiveis = []
    if shutil.which("pdftotext"):
        disponiveis.append("pdftotext")
    for modname in ("pypdf", "PyPDF2"):
        try:
            __import__(modname)
            disponiveis.append(modname)
            break
        except ImportError:
            continue
    return disponiveis


def extract_text(source: "Path | bytes", info: ContentInfo) -> tuple[Optional[str], str]:
    """Extrai o texto de um documento. Devolve (texto, nome_do_extrator)."""
    if info.fmt == "pdf":
        return extract_pdf(source)
    if info.fmt == "rtf":
        data = source if isinstance(source, bytes) else source.read_bytes()
        return extract_rtf(data), "rtf"
    if info.fmt in _ZIP_PARTS:
        return extract_zip_document(source, info.fmt), f"zip:{info.fmt}"
    return None, ""


def print_extractors() -> None:
    pdf = pdf_extractors_disponiveis()
    print("Extratores de texto disponíveis neste ambiente:\n")
    for fmt in sorted(_ZIP_PARTS):
        print(f"  {fmt:10} ok  (biblioteca padrão: zipfile + xml)")
    print(f"  {'rtf':10} ok  (biblioteca padrão)")
    if pdf:
        print(f"  {'pdf':10} ok  (via {' e '.join(pdf)})")
    else:
        print(f"  {'pdf':10} INDISPONÍVEL (PDFs serão pulados)")
        print(f"  {'':10} habilite com: apt install poppler-utils   ou   pip install pypdf")
    print("\nDemais binários (png, elf, zip comum, ole2, ...) são pulados por não terem texto extraível.")
    print("Use --include-binary para escanear os bytes crus mesmo assim (gera muito falso positivo).")


# --------------------------------------------------------------------------- #
# Filtro de ruído textual
#
# Mesmo em arquivos que SÃO texto, blobs codificados (imagem base64 dentro de
# um SVG, anexo de .eml, JS minificado, source map) disparam as regex de hash,
# cartão e documento em massa. O conteúdo é texto, mas não é linguagem, então
# é filtrado antes do casamento, preservando as colunas dos demais achados.
# --------------------------------------------------------------------------- #
def compile_blob_re(min_len: int) -> "Optional[re.Pattern[str]]":
    if min_len <= 0:
        return None
    return re.compile(r"[A-Za-z0-9+/=_\-]{%d,}" % min_len)


@dataclass
class NoiseFilter:
    max_line_len: int = 2000
    blob_re: "Optional[re.Pattern[str]]" = None
    linhas_ignoradas: int = 0
    blobs_mascarados: int = 0

    def apply(self, line: str) -> Optional[str]:
        """Devolve a linha tratada, ou None quando ela toda deve ser ignorada."""
        if self.max_line_len and len(line) > self.max_line_len and " " not in line.strip():
            self.linhas_ignoradas += 1
            return None
        if self.blob_re is not None:
            def mask(m: "re.Match[str]") -> str:
                self.blobs_mascarados += 1
                return " " * (m.end() - m.start())  # preserva colunas
            line = self.blob_re.sub(mask, line)
        return line


# --------------------------------------------------------------------------- #
# Leitura de arquivos (com suporte a arquivos grandes via mmap)
# --------------------------------------------------------------------------- #
def iter_lines_from_path(path: Path, mmap_threshold: int, encoding: str = "utf-8") -> Iterator[tuple[int, str]]:
    """
    Produz (numero_da_linha, texto) sem carregar o arquivo inteiro em uma
    string Python quando ele é grande: usa mmap (memory map) e lê linha a
    linha, o que mantém o uso de memória baixo mesmo para arquivos enormes.
    """
    size = path.stat().st_size
    if size == 0:
        return

    if size >= mmap_threshold:
        with open(path, "rb") as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                for lineno, raw_line in enumerate(iter(mm.readline, b""), start=1):
                    yield lineno, raw_line.decode(encoding, errors="replace")
    else:
        with path.open("r", encoding=encoding, errors="replace") as f:
            for lineno, line in enumerate(f, start=1):
                yield lineno, line


def iter_lines_from_text(texto: str) -> Iterator[tuple[int, str]]:
    for lineno, line in enumerate(texto.splitlines(), start=1):
        yield lineno, line


def scan_lines(
    lines: Iterable[tuple[int, str]],
    source_name: str,
    rules: list[RegexRule],
    max_len: int,
    noise: "Optional[NoiseFilter]" = None,
) -> Iterator[Match]:
    for lineno, line in lines:
        if noise is not None:
            filtrada = noise.apply(line)
            if filtrada is None:
                continue
            line = filtrada
        for rule in rules:
            for m in rule.pattern.finditer(line):
                value = m.group(0)
                if max_len and len(value) > max_len:
                    value = value[:max_len] + "…"
                yield Match(
                    source=source_name,
                    line=lineno,
                    col=m.start() + 1,
                    category=rule.category,
                    description=rule.description,
                    value=value,
                    scope=rule.scope,
                )


@dataclass
class FileOutcome:
    """Resultado do processamento de uma entrada, para o resumo final."""
    matches: list[Match]
    status: str          # "text" | "extracted" | "skipped" | "error" | "empty"
    detalhe: str = ""    # extrator usado, ou motivo de ter sido pulado


def scan_file(
    path: Path,
    rules: list[RegexRule],
    max_len: int,
    mmap_threshold: int,
    extract: bool = True,
    include_binary: bool = False,
    noise: "Optional[NoiseFilter]" = None,
) -> FileOutcome:
    info = sniff_path(path)

    if info.kind == KIND_TEXT:
        try:
            linhas = iter_lines_from_path(path, mmap_threshold, info.encoding)
            return FileOutcome(list(scan_lines(linhas, str(path), rules, max_len, noise)), "text")
        except (OSError, UnicodeError) as e:
            print(f"[!] erro ao ler {path}: {e}", file=sys.stderr)
            return FileOutcome([], "error", str(e))

    if info.kind == KIND_DOCUMENT and extract:
        try:
            texto, extrator = extract_text(path, info)
        except Exception as e:  # extratores externos podem falhar de formas variadas
            print(f"[!] falha ao extrair texto de {path}: {e}", file=sys.stderr)
            texto, extrator = None, ""
        if texto:
            fonte = f"{path}#{extrator}"
            return FileOutcome(
                list(scan_lines(iter_lines_from_text(texto), fonte, rules, max_len, noise)),
                "extracted", extrator,
            )
        if texto is not None:
            return FileOutcome([], "empty", f"{info.fmt}: nenhum texto extraível")
        if info.fmt == "pdf" and not pdf_extractors_disponiveis():
            motivo = "pdf: nenhum extrator disponível (instale poppler-utils ou pypdf)"
        else:
            motivo = f"{info.fmt}: extração falhou"
        if not include_binary:
            print(f"[!] pulado {path}: {motivo}", file=sys.stderr)
            return FileOutcome([], "skipped", motivo)

    if not include_binary:
        return FileOutcome([], "skipped", f"{info.fmt}: {info.reason}")

    # --include-binary: o usuário pediu explicitamente pelos bytes crus.
    try:
        linhas = iter_lines_from_path(path, mmap_threshold, "latin-1")
        return FileOutcome(
            list(scan_lines(linhas, str(path), rules, max_len, noise)), "text", "bytes crus"
        )
    except (OSError, UnicodeError) as e:
        print(f"[!] erro ao ler {path}: {e}", file=sys.stderr)
        return FileOutcome([], "error", str(e))


def scan_stdin(
    rules: list[RegexRule],
    max_len: int,
    extract: bool = True,
    include_binary: bool = False,
    noise: "Optional[NoiseFilter]" = None,
) -> FileOutcome:
    """
    Lê o stdin em modo binário. Iterar sys.stdin em modo texto estoura com
    UnicodeDecodeError assim que alguém encana um PDF para o script.
    """
    data = sys.stdin.buffer.read()
    info = detect_content(data[:SNIFF_SIZE])

    if info.kind == KIND_DOCUMENT and extract:
        try:
            texto, extrator = extract_text(data, info)
        except Exception as e:
            print(f"[!] falha ao extrair texto do stdin: {e}", file=sys.stderr)
            texto, extrator = None, ""
        if texto:
            return FileOutcome(
                list(scan_lines(iter_lines_from_text(texto), f"<stdin>#{extrator}", rules, max_len, noise)),
                "extracted", extrator,
            )
        if texto is None and not include_binary:
            motivo = f"{info.fmt}: nenhum extrator disponível"
            print(f"[!] stdin pulado: {motivo}", file=sys.stderr)
            return FileOutcome([], "skipped", motivo)

    if info.kind == KIND_BINARY and not include_binary:
        motivo = f"{info.fmt}: {info.reason}"
        print(f"[!] stdin parece binário e foi pulado ({motivo}). Use --include-binary para forçar.",
              file=sys.stderr)
        return FileOutcome([], "skipped", motivo)

    encoding = info.encoding or "latin-1"
    texto = data.decode(encoding, errors="replace")
    return FileOutcome(
        list(scan_lines(iter_lines_from_text(texto), "<stdin>", rules, max_len, noise)), "text"
    )


def collect_files(
    paths: list[str],
    recursive: bool,
    exts: Optional[set[str]],
) -> list[Path]:
    """
    Coleta os arquivos a escanear. A classificação texto/documento/binário é
    feita depois, em scan_file, para que valha igualmente para arquivo
    informado direto na linha de comando e para arquivo achado numa pasta.
    antes, o arquivo explícito escapava de qualquer checagem.
    """
    files: list[Path] = []
    for p in paths:
        pp = Path(p)
        if pp.is_dir():
            it = pp.rglob("*") if recursive else pp.glob("*")
            for f in it:
                if not f.is_file():
                    continue
                if exts and f.suffix.lower() not in exts:
                    continue
                files.append(f)
        elif pp.is_file():
            files.append(pp)
        else:
            print(f"[!] caminho não encontrado, ignorado: {p}", file=sys.stderr)
    return files


# --------------------------------------------------------------------------- #
# Memória
# --------------------------------------------------------------------------- #
def apply_memory_limit(mb: int) -> None:
    """
    Tenta ajustar (tipicamente aumentar) o teto de memória virtual do
    processo (RLIMIT_AS), útil quando o script roda sob um ulimit herdado
    restritivo e precisa abrir/mapear arquivos grandes. Só funciona em
    sistemas POSIX (Linux/macOS); em Windows é ignorado com aviso.
    A principal defesa contra estouro de memória em arquivos grandes,
    porém, é o streaming linha a linha via mmap usado no restante do
    script; este limite é apenas um teto de segurança.
    """
    if resource is None:
        print("[!] módulo 'resource' indisponível neste sistema (Windows?); --max-memory-mb ignorado.", file=sys.stderr)
        return
    try:
        limit_bytes = mb * 1024 * 1024
        _soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        new_hard = hard
        if hard != resource.RLIM_INFINITY and hard < limit_bytes:
            new_hard = limit_bytes
        resource.setrlimit(resource.RLIMIT_AS, (limit_bytes, new_hard))
    except (ValueError, OSError) as e:
        print(f"[!] não foi possível ajustar o limite de memória: {e}", file=sys.stderr)


# --------------------------------------------------------------------------- #
# Formatação de saída
# --------------------------------------------------------------------------- #
def pick_desc(m: Match, mode: str) -> str:
    if mode == "short":
        return m.category
    if mode == "both":
        return f"{m.category} ({m.description})"
    return m.description  # long


def write_terminal(m: Match, desc_mode: str, color: bool, fh) -> None:
    desc = pick_desc(m, desc_mode)
    src = colorize(m.source, Color.GREEN, color)
    loc = colorize(f"{m.line}:{m.col}", Color.GRAY, color)
    desc_c = colorize(desc, Color.CYAN, color)
    val = colorize(m.value, Color.YELLOW + Color.BOLD, color)
    print(f"{src} [{loc}] {desc_c} -> {val}", file=fh)


def write_normal(m: Match, desc_mode: str, fh) -> None:
    desc = pick_desc(m, desc_mode)
    print(f"{m.source}\t{m.line}:{m.col}\t{desc}\t{m.value}", file=fh)


def write_values(m: Match, fh) -> None:
    """Só o valor casado, um por linha, para encadear com outra ferramenta."""
    print(m.value, file=fh)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
EPILOG = """\
exemplos:
  # listar todas as categorias disponíveis no JSON
  %(prog)s --list-categories

  # escanear um único arquivo, apenas CPF e e-mail, descrição curta
  %(prog)s relatorio.txt --categories cpf,email --desc short

  # escanear uma pasta inteira, recursivo, com 16 threads, saída em csv
  %(prog)s ./dump --categories cnpj,email,creditCard,apiCredentials \\
      --format csv --out achados.csv --threads 16

  # ler de um pipe (stdin) e gerar JSON
  cat vazamento.log | %(prog)s --format json --desc long

  # só os valores, um por linha, prontos para encadear (deduplicados)
  %(prog)s ./dump --categories cpf --format values

  # uma linha por ocorrência, como o grep -o
  %(prog)s relatorio.txt --format values --keep-duplicates

  # combinar com outras ferramentas
  curl -s https://exemplo.com | %(prog)s --categories email,network
  %(prog)s ./dump --categories email --format values | sort -u > emails.txt
"""


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="osint_regex_scan.py",
        description="Scanner de PII/OSINT usando o dataset osint-brazuca-regex.",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "paths",
        nargs="*",
        help="Arquivo(s) e/ou pasta(s) a escanear. Se omitido, lê da entrada padrão (stdin/pipe).",
    )
    p.add_argument(
        "--json-db",
        nargs="+",
        metavar="CAMINHO",
        help="Um ou mais arquivos JSON de regex, ou uma pasta com eles. "
        f"Padrão: {DB_POR_ESCOPO['br'].name} + {DB_POR_ESCOPO['geral'].name} em {DATASET_DIR}.",
    )
    p.add_argument(
        "--scope",
        choices=["br", "geral", "todos"],
        default="todos",
        help="Contexto do dataset: br=identificadores brasileiros, "
        "geral=padrões universais (wallets, IP, URL, tokens), todos=os dois (padrão).",
    )
    p.add_argument("--list-categories", action="store_true", help="Lista as categorias disponíveis e sai.")

    cat_group = p.add_mutually_exclusive_group()
    cat_group.add_argument("--categories", help="Categorias a usar, separadas por vírgula (ex.: cpf,cnpj,email).")
    cat_group.add_argument("--exclude-categories", help="Categorias a ignorar, separadas por vírgula.")

    p.add_argument("--recursive", dest="recursive", action="store_true", default=True, help="Percorrer subpastas (padrão).")
    p.add_argument("--no-recursive", dest="recursive", action="store_false", help="Não entrar em subpastas.")
    p.add_argument("--ext", help="Extensões a considerar em pastas, separadas por vírgula (ex.: .txt,.log,.csv).")
    p.add_argument(
        "--include-binary",
        action="store_true",
        help="Escaneia os BYTES CRUS de arquivos binários/documentos em vez de pular. "
        "Gera muito falso positivo, use só quando souber o que procura.",
    )
    p.add_argument("--extract", dest="extract", action="store_true", default=True,
                   help="Extrai o texto de documentos (PDF, DOCX, ODT, XLSX, PPTX, EPUB, RTF) antes de casar as regex (padrão).")
    p.add_argument("--no-extract", dest="extract", action="store_false",
                   help="Não extrai texto de documentos; eles passam a ser tratados como binário.")
    p.add_argument("--list-extractors", action="store_true",
                   help="Mostra os extratores de texto disponíveis neste ambiente e sai.")
    p.add_argument("--max-line-len", type=int, default=2000,
                   help="Ignora linhas maiores que N caracteres que não contenham espaço (blob codificado). 0 desativa.")
    p.add_argument("--max-blob-len", type=int, default=512,
                   help="Mascara sequências contínuas de base64/hex com N caracteres ou mais antes de casar. 0 desativa.")

    p.add_argument(
        "--desc",
        choices=["short", "long", "both"],
        default="long",
        help="Detalhe da descrição em terminal/normal: short=chave da categoria, "
        "long=descrição completa do JSON (padrão), both=os dois. "
        "Em csv/json, category e description são sempre incluídos por completo.",
    )
    p.add_argument(
        "--format",
        choices=["terminal", "normal", "csv", "json", "values"],
        default="terminal",
        help="Formato de saída. 'values' imprime apenas o valor casado, um por linha, "
        "pronto para encadear com outra ferramenta (deduplicado por padrão).",
    )
    p.add_argument(
        "--keep-duplicates",
        action="store_true",
        help="Em --format values, imprime uma linha por ocorrência em vez de deduplicar "
        "(equivale ao comportamento do grep -o).",
    )
    p.add_argument("--out", help="Arquivo de saída para csv/json/values (padrão: stdout).")
    p.add_argument("--no-color", action="store_true", help="Desativa cores no formato terminal.")

    p.add_argument("--threads", type=int, default=min(32, (os.cpu_count() or 1) + 4), help="Threads para escanear arquivos de uma pasta em paralelo.")
    p.add_argument(
        "--mmap-threshold-mb",
        type=float,
        default=1.0,
        help="Tamanho (MB) a partir do qual o arquivo é lido via mmap linha a linha em vez de ser carregado inteiro (padrão: 1MB).",
    )
    p.add_argument(
        "--max-memory-mb",
        type=int,
        default=None,
        help="Tenta ajustar/aumentar o teto de memória do processo (RLIMIT_AS), em MB. Só em Linux/macOS.",
    )
    p.add_argument("--max-match-len", type=int, default=300, help="Trunca valores casados maiores que N caracteres (0 = não truncar).")
    p.add_argument("--quiet", action="store_true", help="Não imprime o resumo final em stderr.")
    p.add_argument("--version", action="version", version="osint_regex_scan 1.0.0")
    return p


def main(argv: Optional[list[str]] = None) -> int:
    args = build_arg_parser().parse_args(argv)

    if args.list_extractors:
        print_extractors()
        return 0

    if args.max_memory_mb:
        apply_memory_limit(args.max_memory_mb)

    json_paths = resolver_dbs(args.json_db, args.scope)
    ausentes = [p for p in json_paths if not p.exists()]
    if ausentes:
        for p in ausentes:
            print(f"[erro] arquivo de regex não encontrado: {p}", file=sys.stderr)
        if any(p.name.startswith("osint-brazuca-regex-") for p in ausentes):
            print("       gere-os com: python3 dataset/build.py --split", file=sys.stderr)
        return 2

    if args.list_categories:
        print_categories(json_paths)
        return 0

    include = {x.strip() for x in args.categories.split(",")} if args.categories else None
    exclude = {x.strip() for x in args.exclude_categories.split(",")} if args.exclude_categories else None

    rules, load_errors = load_rules(json_paths, include, exclude)
    for cat, idx, raw_pattern, err in load_errors:
        print(f"[!] regex inválida ignorada [{cat}#{idx}]: {err} -> {raw_pattern}", file=sys.stderr)

    if not rules:
        print("[erro] nenhuma regra de regex carregada (verifique --categories/--json-db).", file=sys.stderr)
        return 2

    color = (not args.no_color) and args.format == "terminal" and sys.stdout.isatty()
    max_len = args.max_match_len
    noise = NoiseFilter(max_line_len=args.max_line_len, blob_re=compile_blob_re(args.max_blob_len))
    status_counts: dict[str, int] = {}
    extratores_usados: dict[str, int] = {}
    pulados: list[tuple[str, str]] = []

    def registrar(nome: str, outcome: FileOutcome) -> None:
        status_counts[outcome.status] = status_counts.get(outcome.status, 0) + 1
        if outcome.status == "extracted" and outcome.detalhe:
            extratores_usados[outcome.detalhe] = extratores_usados.get(outcome.detalhe, 0) + 1
        elif outcome.status in ("skipped", "empty"):
            pulados.append((nome, outcome.detalhe))
    mmap_threshold = int(args.mmap_threshold_mb * 1024 * 1024)

    exts: Optional[set[str]] = None
    if args.ext:
        exts = {e if e.startswith(".") else f".{e}" for e in (x.strip().lower() for x in args.ext.split(","))}

    close_out = False
    out_fh = sys.stdout
    if args.out:
        if args.format in ("csv", "json", "values"):
            out_fh = open(args.out, "w", newline="", encoding="utf-8")
            close_out = True
        else:
            print(f"[!] --out não se aplica ao formato '{args.format}'; a saída vai para stdout.",
                  file=sys.stderr)

    if args.keep_duplicates and args.format != "values":
        print("[!] --keep-duplicates só tem efeito com --format values; ignorado.", file=sys.stderr)

    total_matches = 0
    per_category: dict[str, int] = {}
    valores_vistos: set[str] = set()
    files_scanned = 0
    csv_writer = None
    json_buffer: list[dict] = []

    def emit(m: Match) -> None:
        nonlocal total_matches, csv_writer
        total_matches += 1
        per_category[m.category] = per_category.get(m.category, 0) + 1
        if args.format == "terminal":
            write_terminal(m, args.desc, color, out_fh)
        elif args.format == "normal":
            write_normal(m, args.desc, out_fh)
        elif args.format == "values":
            # Deduplicar preservando a ordem de descoberta = imprimir na primeira
            # ocorrência e ignorar as repetições. Não precisa acumular nem ordenar,
            # então a saída continua saindo em streaming.
            if args.keep_duplicates or m.value not in valores_vistos:
                valores_vistos.add(m.value)
                write_values(m, out_fh)
        elif args.format == "csv":
            if csv_writer is None:
                csv_writer = csv.writer(out_fh)
                csv_writer.writerow(["source", "line", "col", "scope", "category", "description", "value"])
            csv_writer.writerow([m.source, m.line, m.col, m.scope, m.category, m.description, m.value])
        elif args.format == "json":
            json_buffer.append(asdict(m))

    started = time.time()

    use_stdin = not args.paths
    if use_stdin:
        if sys.stdin.isatty():
            print(
                "[erro] nenhum caminho informado e a entrada padrão não é um pipe. "
                "Informe arquivo(s)/pasta(s) ou use: comando | osint_regex_scan.py",
                file=sys.stderr,
            )
            if close_out:
                out_fh.close()
            return 2
        outcome = scan_stdin(rules, max_len, args.extract, args.include_binary, noise)
        for m in outcome.matches:
            emit(m)
        registrar("<stdin>", outcome)
        files_scanned = 1
    else:
        files = collect_files(args.paths, args.recursive, exts)
        if not files:
            print("[erro] nenhum arquivo encontrado nos caminhos informados.", file=sys.stderr)
            if close_out:
                out_fh.close()
            return 2
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            futures = {
                executor.submit(
                    scan_file, f, rules, max_len, mmap_threshold,
                    args.extract, args.include_binary, noise,
                ): f
                for f in files
            }
            for fut in as_completed(futures):
                f = futures[fut]
                outcome = fut.result()
                for m in outcome.matches:
                    emit(m)
                registrar(str(f), outcome)
                files_scanned += 1

    if args.format == "json":
        json.dump(json_buffer, out_fh, ensure_ascii=False, indent=2)
        out_fh.write("\n")

    if close_out:
        out_fh.close()

    if not args.quiet:
        elapsed = time.time() - started
        print(f"\n--- resumo --- arquivos: {files_scanned} | matches: {total_matches} | tempo: {elapsed:.2f}s", file=sys.stderr)

        entrada = []
        if status_counts.get("text"):
            entrada.append(f"texto: {status_counts['text']}")
        if status_counts.get("extracted"):
            detalhe = ", ".join(f"{k}={v}" for k, v in sorted(extratores_usados.items()))
            entrada.append(f"extraídos: {status_counts['extracted']} ({detalhe})")
        if status_counts.get("skipped"):
            entrada.append(f"pulados: {status_counts['skipped']}")
        if status_counts.get("empty"):
            entrada.append(f"sem texto: {status_counts['empty']}")
        if status_counts.get("error"):
            entrada.append(f"erro: {status_counts['error']}")
        if entrada:
            print("  entrada -> " + " | ".join(entrada), file=sys.stderr)

        if args.format == "values" and not args.keep_duplicates and valores_vistos:
            print(f"  valores distintos impressos: {len(valores_vistos)} "
                  f"(de {total_matches} ocorrências)", file=sys.stderr)

        if noise.linhas_ignoradas or noise.blobs_mascarados:
            print(
                f"  ruído filtrado -> linhas ignoradas: {noise.linhas_ignoradas} | "
                f"blobs mascarados: {noise.blobs_mascarados}",
                file=sys.stderr,
            )

        for cat, cnt in sorted(per_category.items(), key=lambda kv: -kv[1]):
            print(f"  {cat}: {cnt}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BrokenPipeError:
        # saída encanada para algo como `head`/`less` que fechou cedo: sair em silêncio
        try:
            sys.stdout.close()
        except Exception:
            pass
        os._exit(0)
