# osint_regex_scan.py

Scanner de regex OSINT baseado no dataset público
[`osint-brazuca-regex`](https://github.com/osintbrazuca/osint-brazuca-regex)
(63 categorias / 346 padrões: CPF, CNPJ, e-mail, telefone, cartões, wallets
cripto, chave PIX, tokens de API/segredos, IPv4/IPv6, domínios .br, .onion,
dados bancários de 26 bancos, etc).

> [!NOTE]
> Requer **Python 3.12+**. Sem dependências externas obrigatórias, só biblioteca padrão.
> Para ampliar o suporte a PDF e à detecção de encoding: `pip install -r requirements.txt`
> (opcional; veja o próprio arquivo para o que cada pacote habilita).

## Arquivos

- `osint_regex_scan.py`: script principal.
- `dataset/osint-brazuca-regex-br.json`: regex de contexto brasileiro (43 categorias, 134 padrões).
- `dataset/osint-brazuca-regex-geral.json`: regex de contexto geral (24 categorias, 212 padrões).
- `dataset/osint-brazuca-regex.json`: união dos dois, **legado/gerado**; o script não o usa por padrão.
- `dataset/build.py`: regenera o unificado a partir dos dois (`--check` valida, `--split` divide).
- `requirements.txt`: pacotes **opcionais** (`pypdf`, `chardet`). O núcleo não precisa de nada.

> [!TIP]
> Por padrão o script carrega os **dois** arquivos por contexto. Use `--scope` para
> restringir, ou `--json-db` para apontar outros caminhos, que aceita vários arquivos
> ou uma pasta.

## Uso rápido

```bash
# listar todas as categorias disponíveis
python3 osint_regex_scan.py --list-categories

# escanear um arquivo, só CPF e e-mail
python3 osint_regex_scan.py relatorio.txt --categories cpf,email

# escanear uma pasta inteira (recursivo), 16 threads, saída csv
python3 osint_regex_scan.py ./dump \
    --categories cnpj,email,creditCard,apiCredentials \
    --format csv --out achados.csv --threads 16

# ler de um pipe (stdin) e gerar JSON
cat vazamento.log | python3 osint_regex_scan.py --format json --desc short

# combinar com outras ferramentas
curl -s https://exemplo.com | python3 osint_regex_scan.py --categories email,network
```

## Opções principais

| Opção | Descrição |
|---|---|
| `paths` | Arquivo(s)/pasta(s). Se omitido, lê de stdin. |
| `--categories a,b,c` | Só usa essas categorias do JSON. |
| `--exclude-categories a,b` | Usa todas menos essas. |
| `--list-categories` | Lista categorias e sai. |
| `--recursive` / `--no-recursive` | Entrar em subpastas (padrão: sim). |
| `--ext .txt,.log` | Filtra extensões ao escanear pastas. |
| `--scope br\|geral\|todos` | Contexto do dataset: só brasileiro, só geral, ou os dois (padrão). |
| `--json-db CAMINHO [CAMINHO ...]` | Um ou mais JSON de regex, ou uma pasta. Padrão: os dois arquivos por contexto. |
| `--include-binary` | Escaneia os **bytes crus** de binários/documentos em vez de pular. Gera muito falso positivo. |
| `--extract` / `--no-extract` | Extrai o texto de documentos antes de casar as regex (padrão: sim). |
| `--list-extractors` | Mostra quais extratores de texto existem neste ambiente e sai. |
| `--max-line-len N` | Ignora linhas maiores que N caracteres sem espaço (blob codificado). `0` desativa. Padrão 2000. |
| `--max-blob-len N` | Mascara sequências contínuas de base64/hex com N+ caracteres. `0` desativa. Padrão 512. |
| `--desc short\|long\|both` | Nível de detalhe da descrição (ver abaixo). |
| `--format terminal\|normal\|csv\|json\|values` | Formato de saída. `values` imprime só o valor casado, um por linha. |
| `--keep-duplicates` | Em `--format values`, uma linha por ocorrência em vez de deduplicar (como `grep -o`). |
| `--out arquivo` | Onde salvar csv/json/values (padrão: stdout). |
| `--no-color` | Desativa cores no formato terminal. |
| `--threads N` | Threads para escanear vários arquivos em paralelo. |
| `--mmap-threshold-mb N` | A partir de qual tamanho o arquivo é lido via mmap linha a linha (padrão 1MB). |
| `--max-memory-mb N` | Tenta ajustar o teto de memória do processo (Linux/macOS). |
| `--max-match-len N` | Trunca valores casados muito longos (padrão 300). |
| `--quiet` | Não imprime o resumo final em stderr. |

## Saída `values` (só o valor)

Para encadear com outra ferramenta, `--format values` imprime **apenas o valor
casado, um por linha**, sem arquivo, linha, coluna nem descrição:

```bash
# lista de CPFs pronta para consumo
python3 osint_regex_scan.py ./dump --categories cpf --format values

# alimentar outro processo
python3 osint_regex_scan.py ./dump --categories email --format values | sort -u > emails.txt
```

Os valores saem **deduplicados**, na ordem em que apareceram: num PDF de teste,
252 ocorrências correspondiam a 203 valores distintos, e a sigla `SE` sozinha
aparecia 25 vezes. Use `--keep-duplicates` para uma linha por ocorrência, como
faz o `grep -o`.

> [!TIP]
> O resumo e os avisos sempre vão para `stderr`, então `stdout` já sai limpo
> para pipe sem precisar de `2>/dev/null`. O resumo informa quantos valores
> distintos foram impressos, para a diferença em relação ao total de achados
> não parecer perda de dado.

> [!NOTE]
> `--max-match-len` (padrão 300) trunca valores longos e marca o corte com `…`.
> Se a saída vai alimentar outro programa, considere `--max-match-len 0` para
> receber o valor inteiro.

## Sobre `--desc` (descrição curta/longa)

O JSON do repositório tem, para cada regex, **uma única** descrição (campo
`description`) dentro de uma categoria (a chave, ex.: `cpf`, `cnpj`,
`email`). Não existem duas versões (curta/longa) da mesma descrição no
arquivo original. Este script resolve isso assim:

- `short` → mostra a **chave da categoria** (ex.: `cpf`, `apiCredentials`).
- `long` → mostra a **descrição completa** do JSON (padrão).
- `both` → mostra os dois juntos.

Isso só afeta os formatos `terminal` e `normal`. Em `csv`/`json` os campos
`category` e `description` são sempre incluídos por completo, para não
perder informação em saídas estruturadas.

## Contexto brasileiro × geral

O dataset é dividido em dois arquivos e o script carrega ambos por padrão:

```bash
python3 osint_regex_scan.py vazamento.log --scope br      # só CPF, CNPJ, PIX, IE, conta bancária...
python3 osint_regex_scan.py codigo/ --scope geral         # só wallets, IP, URL, token de API, hash...
python3 osint_regex_scan.py dump/                         # os dois (padrão)
```

Todo achado carrega o campo `scope` (`br` ou `geral`) nas saídas `csv` e `json`, e
`--list-categories` mostra a coluna de escopo por categoria.

> [!IMPORTANT]
> Quatro categorias existem nos dois arquivos, divididas por entrada: `creditCard`
> (Elo/Hipercard no BR), `socialMedia` (WhatsApp com DDD), `apiCredentials` (Mercado
> Pago, Pagar.me, Asaas) e `vehicles` (ANTT). Elas aparecem como `br+geral` na
> listagem, e o script **mescla** as entradas dos dois arquivos em vez de um
> sobrescrever o outro. Se você escreve seu próprio carregador, replique isso:
> um `dict.update()` simples perde metade das regras dessas categorias.

## Texto, documentos e binários

Regex só faz sentido sobre **texto**. O script classifica cada entrada antes de
escanear, usando **assinatura de conteúdo (número mágico), nunca a extensão**:

| Classe | O que acontece |
|---|---|
| Texto (`.txt`, `.log`, `.csv`, código, JSON...) | Escaneado direto, com o encoding detectado (BOM → UTF-8 → `chardet` se instalado → latin-1). |
| Documento (PDF, DOCX, XLSX, PPTX, ODT, ODS, ODP, EPUB, RTF) | O **texto é extraído** e só ele é escaneado. A origem do achado aparece como `arquivo.pdf#pdftotext`. |
| Demais binários (PNG, ELF, ZIP comum, OLE2, ...) | Pulados, com aviso no resumo. Use `--include-binary` para forçar. |

Extratores: formatos ZIP+XML e RTF usam **só a biblioteca padrão**. PDF tenta,
nesta ordem, o binário `pdftotext` (poppler-utils) e depois `pypdf`/`PyPDF2`;
se nenhum estiver disponível, o PDF é **pulado com instrução de como
habilitar**, nunca escaneado cru.

> [!TIP]
> Rode `--list-extractors` para ver o estado do seu ambiente antes de escanear
> uma pasta cheia de documentos.

> [!CAUTION]
> **Por que isso importa.** Escanear os bytes de um PDF de 66 KB produzia **3.768
> achados**, todos falsos. O `/CreationDate (D:20180514105307)` sozinho casava
> como CNPJ, RENAVAM, RG, telefone, PIS e CTPS ao mesmo tempo. Escaneando o texto
> extraído do mesmo arquivo sobram **72 achados**, e aí aparece um número de
> processo CNJ legítimo que antes ficava afogado no ruído. Use `--include-binary`
> só quando souber exatamente o que procura.

## Filtro de ruído textual

Mesmo em arquivos que **são** texto, blobs codificados disparam as regex de
hash, cartão e documento em massa: imagem base64 dentro de um SVG, anexo de
`.eml`, JavaScript minificado, source map. O script trata isso antes do
casamento:

- Linha maior que `--max-line-len` **sem nenhum espaço** → ignorada.
- Sequência contínua de base64/hex com `--max-blob-len` caracteres ou mais →
  mascarada (preservando as colunas do restante da linha).

Ambos aparecem no resumo final e podem ser desativados com `0`.

## Detalhes de implementação

- **Arquivos grandes / memória**: cada arquivo é aberto com `mmap` e lido
  linha a linha (`mmap.readline`), então o conteúdo nunca é carregado
  inteiro numa string Python, e o uso de memória fica proporcional a uma
  linha, não ao arquivo inteiro. `--max-memory-mb` complementa isso
  tentando levantar o teto de memória do processo (`RLIMIT_AS`) via
  `resource.setrlimit`, mas só funciona em Linux/macOS.
- **Multi-thread**: ao escanear uma pasta, cada arquivo é processado em
  paralelo com `ThreadPoolExecutor` (`--threads`).
- **Normalização de regex**: duas regras do JSON usam sintaxe que o `re`
  do Python não aceita direto:
  - `correios`: vem no formato JS `/padrao/i`, e o script extrai o padrão e
    a flag e compila corretamente.
  - `crm`: tem um `(?i)` no meio do padrão, o que o Python 3.11+ rejeita
    (`global flags not at the start of the expression`), e o script extrai
    a flag e aplica globalmente via `re.compile(pattern, re.IGNORECASE)`.

  Todos os 346 padrões do JSON foram testados e compilam corretamente após
  essa normalização.

## Observação sobre falsos positivos

Algumas regex do dataset são propositalmente "soltas" (sem âncoras nem
contexto), por exemplo `cpf` aceita qualquer sequência de 11 dígitos com
pontuação opcional, e `cnes`/`codigoIbge`/`chaveNfe` são só `\d{7}`/`\d{44}`.
Isso é uma característica do dataset original, não um bug deste script;
ao escanear textos com muitos números (logs, planilhas), espere bastante
ruído nessas categorias.

> [!CAUTION]
> Um achado **não** é PII confirmada: as regex conferem formato, não dígito
> verificador. Combine `--categories` (ou `--scope`) com bom senso e revise os
> resultados antes de tratá-los como dado pessoal real.
