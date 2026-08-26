#!/usr/bin/env python3
"""
build.py: gerador do dataset osint-brazuca-regex
=================================================

O dataset é editado em DOIS arquivos, por contexto:

  osint-brazuca-regex-br.json     identificadores brasileiros (CPF, CNPJ, PIX,
                                  IE por UF, contas bancárias, ...)
  osint-brazuca-regex-geral.json  padrões universais (wallets cripto, IP, URL,
                                  domínio, tokens de API, hashes, ...)

O arquivo osint-brazuca-regex.json é a UNIÃO dos dois, mantido como artefato
GERADO por compatibilidade com quem já consome a URL crua do repositório.
Editar o unificado à mão não adianta: o próximo build sobrescreve.

Uso:
    python3 dataset/build.py            # regenera o unificado a partir dos dois
    python3 dataset/build.py --check    # valida sem escrever (bom para CI)
    python3 dataset/build.py --split    # divide o unificado nos dois (migração)

Sem dependências externas.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

DATASET_DIR = Path(__file__).resolve().parent
UNIFICADO = DATASET_DIR / "osint-brazuca-regex.json"
BR = DATASET_DIR / "osint-brazuca-regex-br.json"
GERAL = DATASET_DIR / "osint-brazuca-regex-geral.json"

# --------------------------------------------------------------------------- #
# Classificação
#
# Mapa explícito de propósito: uma categoria nova que não esteja aqui faz o
# build falhar, em vez de cair silenciosamente no arquivo errado.
# --------------------------------------------------------------------------- #
CATEGORIAS_BR: frozenset[str] = frozenset({
    "boleto", "cadastur", "cep", "cepPorUf", "cnpj", "cnpjAlfanumerico",
    "cnpjOuCpf", "cnpjAlfanamuericoOuCpf", "cnh", "cpf", "cpfPorUf", "crm",
    "ie", "pixChave", "pixChaveRandom", "placaDetran", "renavam", "rg", "rne",
    "siglaUF", "telefone", "processoCnj", "numeroDeEndereco", "bankAccount",
    "tituloEleitor", "pisPasep", "cartaoSus", "cnes", "inscricaoMunicipal",
    "codigoIbge", "cns", "ctps", "chaveNfe", "identificadoresGov", "business",
    "education", "documentsAdditional", "passaporte", "rastreamentoCorreios",
})

CATEGORIAS_GERAL: frozenset[str] = frozenset({
    "cryptoWallets", "network", "infraCloud", "torDarkWeb", "creditCard",
    "socialMedia", "apiCredentials", "vehicles", "security", "databaseUrls",
    "containerSecrets", "privateKeys", "sensitivePatterns", "internalUrls",
    "geolocation", "financialInternational", "data", "email", "hora12",
    "hora24", "UUID", "verificacaoDeSenha", "isbn", "ean13",
})

# Categorias de contexto geral que contêm entradas especificamente brasileiras.
# A chave da categoria existe nos dois arquivos; a descrição decide o lado.
ENTRADAS_BR_EM_CATEGORIA_GERAL: dict[str, tuple[str, ...]] = {
    "creditCard": ("Elo -", "Hipercard -"),
    "socialMedia": ("WhatsApp - Links com número brasileiro",),
    "apiCredentials": ("Mercado Pago Access Token", "Pagar.me API Key", "Asaas API Key"),
    "vehicles": ("ANTT -",),
}


def eh_entrada_br(categoria: str, descricao: str) -> bool:
    for prefixo in ENTRADAS_BR_EM_CATEGORIA_GERAL.get(categoria, ()):
        if descricao.startswith(prefixo):
            return True
    return False


def validar_cobertura(categorias: list[str]) -> None:
    conhecidas = CATEGORIAS_BR | CATEGORIAS_GERAL
    faltando = [c for c in categorias if c not in conhecidas]
    if faltando:
        raise SystemExit(
            "[erro] categoria sem classificação em build.py: "
            + ", ".join(faltando)
            + "\n       adicione em CATEGORIAS_BR ou CATEGORIAS_GERAL."
        )
    sobrando = sorted(conhecidas - set(categorias))
    if sobrando:
        print(f"[!] classificadas mas ausentes do dataset: {', '.join(sobrando)}", file=sys.stderr)


def carregar(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f, object_pairs_hook=collections.OrderedDict)


def escrever(path: Path, dados: dict) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
        f.write("\n")


# --------------------------------------------------------------------------- #
# Split: unificado -> br + geral
# --------------------------------------------------------------------------- #
def dividir(uni: dict) -> tuple[dict, dict]:
    validar_cobertura(list(uni))
    br: dict = collections.OrderedDict()
    geral: dict = collections.OrderedDict()

    for categoria, entradas in uni.items():
        if categoria in CATEGORIAS_BR:
            br[categoria] = list(entradas)
            continue
        if categoria not in ENTRADAS_BR_EM_CATEGORIA_GERAL:
            geral[categoria] = list(entradas)
            continue
        # categoria dividida por entrada
        so_br = [e for e in entradas if eh_entrada_br(categoria, e["description"])]
        so_geral = [e for e in entradas if not eh_entrada_br(categoria, e["description"])]
        esperado = len(ENTRADAS_BR_EM_CATEGORIA_GERAL[categoria])
        if len(so_br) != esperado:
            raise SystemExit(
                f"[erro] {categoria}: esperava {esperado} entrada(s) brasileira(s), "
                f"encontrei {len(so_br)}. Ajuste ENTRADAS_BR_EM_CATEGORIA_GERAL."
            )
        if so_br:
            br[categoria] = so_br
        if so_geral:
            geral[categoria] = so_geral

    return br, geral


# --------------------------------------------------------------------------- #
# Merge: br + geral -> unificado
#
# A ordem das categorias e a ordem das entradas dentro de cada categoria
# seguem o arquivo unificado atual, para que o merge seja idempotente e o
# diff da migração fique vazio.
# --------------------------------------------------------------------------- #
def mesclar(br: dict, geral: dict, referencia: "dict | None" = None) -> dict:
    ordem_categorias = list(referencia) if referencia else list(geral) + [
        c for c in br if c not in geral
    ]
    for c in list(br) + list(geral):
        if c not in ordem_categorias:
            ordem_categorias.append(c)

    uni: dict = collections.OrderedDict()
    for categoria in ordem_categorias:
        entradas = list(geral.get(categoria, [])) + list(br.get(categoria, []))
        if not entradas:
            continue
        if referencia and categoria in referencia:
            # restaura a posição original das entradas dentro da categoria
            posicao = {
                (e["regex"], e["description"]): i
                for i, e in enumerate(referencia[categoria])
            }
            entradas.sort(key=lambda e: posicao.get((e["regex"], e["description"]), 10**6))
        uni[categoria] = entradas
    return uni


# --------------------------------------------------------------------------- #
# Relatório
# --------------------------------------------------------------------------- #
def resumo(br: dict, geral: dict) -> None:
    nbr = sum(len(v) for v in br.values())
    nger = sum(len(v) for v in geral.values())
    print(f"  br    : {len(br):>2} categorias, {nbr:>3} entradas  -> {BR.name}")
    print(f"  geral : {len(geral):>2} categorias, {nger:>3} entradas  -> {GERAL.name}")
    compartilhadas = sorted(set(br) & set(geral))
    if compartilhadas:
        print(f"  divididas por entrada: {', '.join(compartilhadas)}")
    print(f"  total : {nbr + nger} entradas")


def conferir_integridade(br: dict, geral: dict, uni: dict) -> list[str]:
    problemas: list[str] = []

    chave = lambda d: sorted((c, e["regex"], e["description"]) for c, v in d.items() for e in v)
    if sorted(chave(br) + chave(geral)) != chave(uni):
        problemas.append("conteúdo de br+geral difere do unificado")

    for nome, dados in (("br", br), ("geral", geral), ("unificado", uni)):
        for categoria, entradas in dados.items():
            for e in entradas:
                if set(e) != {"regex", "description"}:
                    problemas.append(f"{nome}/{categoria}: schema inesperado {sorted(e)}")
                try:
                    re.compile(e["regex"])
                except re.error as err:
                    problemas.append(f"{nome}/{categoria}: regex não compila ({err})")
        contagem = collections.Counter(e["regex"] for v in dados.values() for e in v)
        for regex, n in contagem.items():
            if n > 1:
                problemas.append(f"{nome}: regex duplicada {n}x -> {regex[:50]}")

    return problemas


def main(argv: "list[str] | None" = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[1],
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    modo = p.add_mutually_exclusive_group()
    modo.add_argument("--split", action="store_true",
                      help="Divide o unificado em br/geral (migração inicial).")
    modo.add_argument("--check", action="store_true",
                      help="Valida a coerência entre os três arquivos sem escrever nada.")
    args = p.parse_args(argv)

    if args.split:
        uni = carregar(UNIFICADO)
        br, geral = dividir(uni)
        escrever(BR, br)
        escrever(GERAL, geral)
        print("dividido:")
        resumo(br, geral)
        problemas = conferir_integridade(br, geral, uni)
        if problemas:
            print("\n[erro] integridade:", file=sys.stderr)
            for x in problemas:
                print("  -", x, file=sys.stderr)
            return 1
        print("  integridade: ok")
        return 0

    for arquivo in (BR, GERAL):
        if not arquivo.exists():
            print(f"[erro] {arquivo} não existe. Rode primeiro: python3 {Path(__file__).name} --split",
                  file=sys.stderr)
            return 2

    br, geral = carregar(BR), carregar(GERAL)
    validar_cobertura(sorted(set(br) | set(geral)))
    referencia = carregar(UNIFICADO) if UNIFICADO.exists() else None
    uni = mesclar(br, geral, referencia)

    problemas = conferir_integridade(br, geral, uni)
    if problemas:
        print("[erro] integridade:", file=sys.stderr)
        for x in problemas:
            print("  -", x, file=sys.stderr)
        return 1

    novo = json.dumps(uni, indent=4, ensure_ascii=False) + "\n"
    atual = UNIFICADO.read_text(encoding="utf-8") if UNIFICADO.exists() else None

    if args.check:
        resumo(br, geral)
        print("  integridade: ok")
        if atual is not None and atual != novo:
            print(f"[erro] {UNIFICADO.name} está desatualizado. Rode: python3 dataset/build.py",
                  file=sys.stderr)
            return 1
        print(f"  {UNIFICADO.name}: em dia")
        return 0

    if atual == novo:
        resumo(br, geral)
        print(f"  {UNIFICADO.name}: já estava em dia (nada a fazer)")
        return 0

    UNIFICADO.write_text(novo, encoding="utf-8")
    resumo(br, geral)
    print(f"  {UNIFICADO.name}: regenerado")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
