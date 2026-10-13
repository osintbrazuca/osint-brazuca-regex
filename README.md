<h1 align="center">OSINT Brazuca Regex</h1>

<p align="center">
  Repositório criado com o intuito de reunir <b>expressões regulares</b> focadas no contexto brasileiro 🇧🇷 e geral.
</p>

<h1 align="center">
  <br>
  <a href="https://nuclei.projectdiscovery.io"><img src="assets/logo_profile.png" width="300px" alt="OSINT Brazuca"></a>
</h1>


<p align="center">
<a href="./dataset/osint-brazuca-regex-br.json"><img alt="Regex Brasil" src="https://img.shields.io/badge/Brasil-134_regex-1E88E5?style=for-the-badge&logo=awesomelists&logoColor=white"></a>
<a href="./dataset/osint-brazuca-regex-geral.json"><img alt="Regex Geral" src="https://img.shields.io/badge/Geral-212_regex-2E7D32?style=for-the-badge&logo=bookstack&logoColor=white"></a>
<a href="./dataset/osint-brazuca-regex.json"><img alt="Formato" src="https://img.shields.io/badge/Formato-JSON-EF6C00?style=for-the-badge&logo=json&logoColor=white"></a>
<a href="#introdução"><img alt="OSINT Brasil" src="https://img.shields.io/badge/OSINT-Brasil-00838F?style=for-the-badge&logo=googleearth&logoColor=white"></a>
</p>

<p align="center">
<a href="https://github.com/osintbrazuca/osint-brazuca-regex/blob/main/LICENSE"><img alt="Licença" src="https://img.shields.io/github/license/osintbrazuca/osint-brazuca-regex?style=for-the-badge&color=1E88E5&logo=opensourceinitiative&logoColor=white"></a>
<a href="https://github.com/osintbrazuca/osint-brazuca-regex/graphs/contributors"><img alt="Contribuidores" src="https://img.shields.io/github/contributors-anon/osintbrazuca/osint-brazuca-regex?style=for-the-badge&color=2E7D32&logo=github&logoColor=white"></a>
<a href="https://github.com/osintbrazuca/osint-brazuca-regex/issues"><img alt="Issues abertas" src="https://img.shields.io/github/issues-raw/osintbrazuca/osint-brazuca-regex?style=for-the-badge&color=EF6C00&logo=github&logoColor=white"></a>
<a href="https://github.com/osintbrazuca/osint-brazuca-regex/discussions"><img alt="Discussões" src="https://img.shields.io/github/discussions/osintbrazuca/osint-brazuca-regex?style=for-the-badge&color=6A1B9A&logo=github&logoColor=white"></a>
<a href="https://github.com/osintbrazuca/osint-brazuca-regex/network/members"><img alt="Forks" src="https://img.shields.io/github/forks/osintbrazuca/osint-brazuca-regex?style=for-the-badge&color=00838F&logo=github&logoColor=white"></a>
<a href="https://github.com/osintbrazuca/osint-brazuca-regex/stargazers"><img alt="Estrelas" src="https://img.shields.io/github/stars/osintbrazuca/osint-brazuca-regex?style=for-the-badge&color=F9A825&logo=github&logoColor=white"></a>
</p>


# Introdução
**OSINT Brazuca Regex** é um repositório criado com o intuito de reunir **expressões regulares** focadas no contexto brasileiro 🇧🇷 e internacional. Seu objetivo é auxiliar analistas e pesquisadores de OSINT a filtrar e identificar informações relevantes durante processos de coleta e análise massiva de dados.

### Contexto
Todo analista de OSINT / Intel que efetua coletas massivas de dados ou precisa realizar checagem de informações em grandes volumes (arquivos) enfrenta a dificuldade de filtrar os dados relevantes. 

Para filtrar os dados é necessário definir uma chave de busca, que pode ser uma string de interesse ou documentos específicos do negócio. Frequentemente precisamos recorrer a expressões regulares específicas do contexto brasileiro ou consultar documentação interna.

O **OSINT Brazuca Regex** tem o objetivo de facilitar esse processo, organizando expressões regulares de interesse para checagem em massa usando os padrões selecionados. Você analista pode fazer o fork do projeto e criar suas proprias seções nos arquivos /dataset/*.json ou criar um aquivo isoado para seu contexto (exemplo: /dataset/teste.json).



As regex são mantidas em **dois arquivos, por contexto**. Use o que fizer sentido para o seu caso:

| Arquivo | Conteúdo | Categorias | Regex |
|---|---|---|---|
| [`osint-brazuca-regex-br.json`](./dataset/osint-brazuca-regex-br.json) | Identificadores brasileiros: CPF, CNPJ, PIX, IE por UF, contas bancárias, CNH, título de eleitor, processo CNJ... | 43 | 134 |
| [`osint-brazuca-regex-geral.json`](./dataset/osint-brazuca-regex-geral.json) | Padrões universais: wallets cripto, IPv4/IPv6, domínios, URLs, tokens de API, hashes, redes sociais... | 24 | 212 |

> [!NOTE]
> Quatro categorias (`creditCard`, `socialMedia`, `apiCredentials`, `vehicles`) existem nos **dois** arquivos: a parte brasileira (Elo, Hipercard, WhatsApp com DDD, Mercado Pago, Pagar.me, Asaas, ANTT) fica no arquivo BR, o resto no geral.

> [!WARNING]
> **Sem rede**. Não há consultas, verificadores ou qualquer interação com APIs externas; toda validação é realizada localmente, com regex e Python.

> [!WARNING]
> **Arquivo legado.** O [`osint-brazuca-regex.json`](./dataset/osint-brazuca-regex.json) unificado continua disponível, com as 346 regex, para não quebrar quem já consome a URL crua. Ele passou a ser **um artefato gerado** a partir dos dois arquivos acima (`python3 dataset/build.py`) e está descontinuado; novos consumidores devem apontar para os arquivos separados.

> [!IMPORTANT]
> **Compatibilidade de engine.** Algumas expressões usam a flag inline `(?i)` no início do padrão e outras usam _lookaround_ (`(?=`, `(?!`, `(?<!`). A flag inline funciona em Python, PCRE e Go, mas **não** é aceita pelo `RegExp` do JavaScript. Nesse caso, remova o `(?i)` e passe a flag `i` na construção da expressão. _Lookaround_ não é suportado pelo RE2 (Go).

> [!CAUTION]
> **Estas expressões conferem formato, não dígito verificador.** CPF, CNPJ, PIS, CNS, EAN-13 e boleto precisam da checagem aritmética de DV do lado de quem consome. Um match aqui **não** é um documento válido, e tratá-lo como PII confirmada leva a falso positivo.

<br>

# Índice
- [Ferramentas](#ferramentas)
- [Documentos Brasileiros](#documentos-brasileiros)
- [Identificadores Governamentais](#identificadores-gov)
- [Criptomoedas e Wallets](#criptomoedas-wallets)
- [Network e Infraestrutura](#network-infraestrutura)
- [Cartões de Crédito](#cartoes-credito)
- [Dados Bancários](#dados-bancarios)
- [Tor e Dark Web](#tor-darkweb)
- [Redes Sociais e Mensageria](#redes-sociais)
- [Geolocalização](#geolocalizacao)
- [Veículos, Negócios e Educação](#veiculos-negocios-educacao)
- [Documentos Complementares](#documentos-complementares)
- [Financeiro Internacional](#financeiro-internacional)
- [Hashes e Tokens](#hashes-tokens)
- [Credenciais de API e Segredos](#credenciais-api)
- [Bancos de Dados e Containers](#bancos-containers)
- [Chaves Privadas e Certificados](#chaves-privadas)
- [Padrões Sensíveis e URLs Internas](#padroes-sensiveis)
- [REGEX Genéricas](#regex-genericas)

<br>


# Ferramentas <a name="ferramentas"></a>

## osint_regex_scan.py

Scanner que aplica o dataset deste repositório sobre arquivos, pastas ou entrada via `stdin`. Requer **Python 3.12+** e não tem dependências obrigatórias. Documentação completa em [tool.md](tool.md); os pacotes opcionais estão em [requirements.txt](requirements.txt).

```bash
# listar as categorias disponíveis
python3 osint_regex_scan.py --list-categories

# escanear um arquivo, apenas CPF e e-mail
python3 osint_regex_scan.py relatorio.txt --categories cpf,email

# usar só as regex de contexto brasileiro (ou só as gerais)
python3 osint_regex_scan.py relatorio.txt --scope br

# só os valores encontrados, um por linha, prontos para encadear
python3 osint_regex_scan.py ./dump --categories cpf --format values

# escanear uma pasta inteira, saída em CSV
python3 osint_regex_scan.py ./dump --categories cnpj,email,creditCard,apiCredentials \
    --format csv --out achados.csv --threads 16

# escanear uma pasta inteira, seta categoria especifica, usa arquivo teste como base regex, saída em valores, 
python3 osint_regex_scan.py ./dump --categories meus_vips --js-db ./dataset/teste.json --format values
```

> [!TIP]
> O scanner só casa regex sobre **texto**: PDF, DOCX, XLSX, ODT, EPUB e RTF têm o texto extraído antes; demais binários são pulados. Rode `--list-extractors` para ver o que está disponível no seu ambiente.

Também é possível instalar o scanner com o [OTinstaller](https://github.com/OSINTVerseHQ/OTinstaller), um gerenciador de ferramentas de terceiros para Linux que instala este repositório em um virtualenv próprio (requer Python 3.12+, como o scanner). O OTinstaller não é mantido por este projeto; problemas com ele devem ser relatados [no repositório do OTinstaller](https://github.com/OSINTVerseHQ/OTinstaller/issues).

```bash
pipx install otinstaller
otinstaller install osint-brazuca-regex
otinstaller run osint-brazuca-regex -- relatorio.txt --categories cpf,email
```

<h1 align="center">
  <a href="./tool.md"><img src="assets/01.png" alt="OSINT Brazuca"></a>
</h1>


# Documentos Brasileiros <a name="documentos-brasileiros"></a>

## CNPJ - Cadastro Nacional da Pessoa Jurídica
```
\b\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}\b|\b\d{14}\b
```

## CNPJ Alfanumérico - Cadastro Nacional da Pessoa Jurídica (Válido a partir de Julho de 2026)
```
^([A-Za-z0-9]{2}[\.]?[A-Za-z0-9]{3}[\.]?[A-Za-z0-9]{3}[\/]?[A-Za-z0-9]{4}[-]?\d{2})$
```

## CPF - Cadastro de Pessoas Físicas
```
\b\d{3}\.\d{3}\.\d{3}-\d{2}\b|\b\d{11}\b
```

## Título de Eleitor
```
\b\d{4}\s?\d{4}\s?\d{4}\b
```

## PIS/PASEP/NIT - Programa de Integração Social
```
\d{3}\.?\d{5}\.?\d{2}[-\s]?\d{1}
```

## Cartão SUS - Cartão Nacional de Saúde
```
\b\d{3}\s?\d{4}\s?\d{4}\s?\d{4}\b
```

## CNES - Cadastro Nacional de Estabelecimentos de Saúde
```
(?:CNES|cnes)[\s.:nº°-]{0,6}(\d{7})\b
```

## CNS - Cartão Nacional de Saúde (formato validado)
```
[1-2]\d{10}00[0-1]\d|[7-9]\d{14}
```

## CTPS - Carteira de Trabalho e Previdência Social
```
\d{7}\s?(\d{5})?
```

## Código IBGE - Código de Município (7 dígitos)
```
(?:IBGE|ibge)[\s.:nº°-]{0,6}(\d{7})\b
```

## Inscrição Municipal
```
(?:IM|[Ii]nscrição [Mm]unicipal|CCM)[\s.:nº°-]{0,6}(\d{6,15})\b
```
### CPF - Cadastro de Pessoas Físicas por Localidade
<details>
  <summary>Rio Grande do Sul</summary>
  <br>
  Dígito <b>0</b>
  <p>Ex: 999.999.99<ins>0</ins>-99</p>
  <pre>^\d{3}\.?\d{3}\.?\d{2}0-?\d{2}$</pre>
  <br>
</details>
<details>
  <summary>Distrito Federal, Goiás, Mato Grosso, Mato Grosso do Sul e Tocantins</summary>
  <br>
  Dígito <b>1</b>
  <p>Ex: 000.000.00<ins>1</ins>-00</p>
  <pre>^\d{3}\.?\d{3}\.?\d{2}1-?\d{2}$</pre>
  <br>
</details>
<details>
  <summary>Amazonas, Pará, Roraima, Amapá, Acre e Rondônia</summary>
  <br>
  Dígito <b>2</b>
  <p>Ex: 000.000.00<ins>2</ins>-00</p>
  <pre>^\d{3}\.?\d{3}\.?\d{2}2-?\d{2}$</pre>
  <br>
</details>
<details>
  <summary>Ceará, Maranhão e Piauí</summary>
  <br>
  Dígito <b>3</b>
  <p>Ex: 000.000.00<ins>3</ins>-00</p>
  <pre>^\d{3}\.?\d{3}\.?\d{2}3-?\d{2}$</pre>
  <br>
</details>
<details>
  <summary>Paraíba, Pernambuco, Alagoas e Rio Grande do Norte</summary>
  <br>
  Dígito <b>4</b>
  <p>Ex: 000.000.00<ins>4</ins>-00</p>
  <pre>^\d{3}\.?\d{3}\.?\d{2}4-?\d{2}$</pre>
  <br>
</details>
<details>
  <summary>Bahia e Sergipe</summary>
  <br>
  Dígito <b>5</b>
  <p>Ex: 000.000.00<ins>5</ins>-00</p>
  <pre>^\d{3}\.?\d{3}\.?\d{2}5-?\d{2}$</pre>
  <br>
</details>
<details>
  <summary>Minas Gerais</summary>
  <br>
  Dígito <b>6</b>
  <p>Ex: 000.000.00<ins>6</ins>-00</p>
  <pre>^\d{3}\.?\d{3}\.?\d{2}6-?\d{2}$</pre>
  <br>
</details>
<details>
  <summary>Rio de Janeiro e Espírito Santo</summary>
  <br>
  Dígito <b>7</b>
  <p>Ex: 000.000.00<ins>7</ins>-00</p>
  <pre>^\d{3}\.?\d{3}\.?\d{2}7-?\d{2}$</pre>
  <br>
</details>
<details>
  <summary>São Paulo</summary>
  <br>
  Dígito <b>8</b>
  <p>Ex: 000.000.00<ins>8</ins>-00</p>
  <pre>^\d{3}\.?\d{3}\.?\d{2}8-?\d{2}$</pre>
  <br>
</details>
<details>
  <summary>Paraná e Santa Catarina</summary>
  <br>
  Dígito <b>9</b>
  <p>Ex: 000.000.00<ins>9</ins>-00</p>
  <pre>^\d{3}\.?\d{3}\.?\d{2}9-?\d{2}$</pre>
  <br>
</details>



## RG - Registro Geral 
```
(\d{1,2}\.?)(\d{3}\.?)(\d{3})(\-?[0-9Xx]{1})
```

## CNH - Carteira Nacional de Habilitação
```
(?:CNH|cnh|[Hh]abilitação|[Cc]arteira)\D{0,15}(\d{11})\b
```

## CEP - Código de Endereçamento Postal 
```
(^[0-9]{5})-?([0-9]{3}$)
```

### CEP - Código de Endereçamento Postal por localidade

  * Centro-Oeste
    <details>
      <summary>Distrito Federal</summary>
      <br>
      70000-000 a 72799-999 e 73000-000 a 73699-999
      <pre>\b7(?:[0-2][0-7]|3[0-6])\d{2}-?\d{3}\b</pre>
      <br>
    </details>
    <details>
      <summary>Goiás</summary>
      <br>
      72800-000 a 72999-999 e 73700-000 a 76799-999
      <pre>\b7(?:2[89]|3[7-9]|[45]\d|6[0-7])\d{2}-?\d{3}\b</pre>
      <br>
    </details>
    <details>
      <summary>Mato Grosso do Sul</summary>
      <br>
      79000-000 a 79999-999
      <pre>\b79\d{3}-?\d{3}\b</pre>
      <br>
    </details>
    <details>
      <summary>Mato Grosso</summary>
      <br>
      78000-000 a 78899-999
      <pre>\b78[0-8]\d{2}-?\d{3}\b</pre>
      <br>
    </details>

  * Nordeste

    <details>
      <summary>Alagoas</summary>
      <br>
      57000-000 a 57999-999
      <pre>\b57\d{3}-?\d{3}\b</pre>
      <br>
    </details>
    <details>
      <summary>Bahia</summary>
      <br>
      40000-000 a 48999-999
      <pre>\b4[0-8]\d{3}-?\d{3}\b</pre>
      <br>
    </details>
    <details>
      <summary>Ceará</summary>
      <br>
      60000-000 a 63999-999
      <pre>\b6[0-3]\d{3}-?\d{3}\b</pre>
      <br>
    </details>
      <details>
      <summary>Maranhão</summary>
      <br>
      65000-000 a 65999-999
      <pre>\b65\d{3}-?\d{3}\b</pre>
      <br>
    </details>
    <details>
      <summary>Paraíba</summary>
      <br>
      58000-000 a 58999-999
      <pre>\b58\d{3}-?\d{3}\b</pre>
      <br>
    </details>
    <details>
      <summary>Pernambuco</summary>
      <br>
      50000-000 a 56999-999
      <pre>\b5[0-6]\d{3}-?\d{3}\b</pre>
      <br>
    </details>
    <details>
      <summary>Piauí</summary>
      <br>
      64000-000 a 64999-999
      <pre>\b64\d{3}-?\d{3}\b</pre>
      <br>
    </details>
    <details>
      <summary>Rio Grande do Norte</summary>
      <br>
      59000-000 a 59999-999
      <pre>\b59\d{3}-?\d{3}\b</pre>
      <br>
    </details>
    <details>
      <summary>Sergipe</summary>
      <br>
      49000-000 a 49999-999
      <pre>\b49\d{3}-?\d{3}\b</pre>
      <br>
    </details>

  * Norte
    <details>
      <summary>Acre</summary>
      <br>
      69900-000 a 69999-999
      <pre>\b699\d{2}-?\d{3}\b</pre>
      <br>
    </details>
    <details>
      <summary>Amapá</summary>
      <br>
      68900-000 a 68999-999
      <pre>\b689\d{2}-?\d{3}\b</pre>
      <br>
    </details>
    <details>
      <summary>Amazonas</summary>
      <br>
      69000-000 a 69299-999 e 69400-000 a 69899-999
      <pre>\b69(?:[0-2]|[4-8])\d{2}-?\d{3}\b</pre>
      <br>
    </details>
    <details>
      <summary>Pará</summary>
      <br>
      66000-000 a 68899-999
      <pre>\b(?:6[6-7]\d{3}|68[0-8]\d{2})-?\d{3}\b</pre>
      <br>
    </details>
    <details>
      <summary>Rondônia</summary>
      <br>
      76800-000 a 76999-999
      <pre>\b76[89]\d{2}-?\d{3}\b</pre>
      <br>
    </details>
    <details>
      <summary>Roraima</summary>
      <br>
      69300-000 a 69399-999
      <pre>\b693\d{2}-?\d{3}\b</pre>
      <br>
    </details>
    <details>
      <summary>Tocantins</summary>
      <br>
      77000-000 a 77999-999
      <pre>\b77\d{3}-?\d{3}\b</pre>
      <br>
    </details>

  * Sudeste
    <details>
      <summary>Espírito Santo</summary>
      <br>
      29000-000 a 29999-999
      <pre>\b29\d{3}-?\d{3}\b</pre>
      <br>
    </details>
    <details>
      <summary>Minas Gerais</summary>
      <br>
      30000-000 a 39999-999
      <pre>\b3\d{4}-?\d{3}\b</pre>
      <br>
    </details>
    <details>
      <summary>Rio de Janeiro</summary>
      <br>
      20000-000 a 28999-999
      <pre>\b2[0-8]\d{3}-?\d{3}\b</pre>
      <br>
    </details>
    <details>
      <summary>São Paulo</summary>
      <br>
      01000-000 a 19999-999
      <pre>\b(?:0[1-9]\d{3}|1\d{4})-?\d{3}\b</pre>
      <br>
    </details>

  * Sul
    <details>
      <summary>Paraná</summary>
      <br>
      80000-000 a 87999-999
      <pre>\b8[0-7]\d{3}-?\d{3}\b</pre>
      <br>
    </details>
    <details>
      <summary>Rio Grande do Sul</summary>
      <br>
      90000-000 a 99999-999
      <pre>\b9\d{4}-?\d{3}\b</pre>
      <br>
    </details>
    <details>
      <summary>Santa Catarina</summary>
      <br>
      88000-000 a 89999-999
      <pre>\b8[89]\d{3}-?\d{3}\b</pre>
      <br>
    </details>

## RNE - Registro Nacional de Estrangeiro
```
(RNE)([A-Z\d])(\d{6})([A-Z\d])
```

## RENAVAM - Registro Nacional de Veículos Automotores
```
((\d{4})[.](\d{6})-(\d{1})|(\d{4})(\d{6})(\d{1}))
```

## Placas de Veículos Automotores - Modelo Mercosul e Modelo Antigo
```
\b[A-Za-z]{3}-?\d[A-Za-z0-9]\d{2}\b
```

## Boleto Bancário e Linha Digitável
```
(\d{5}[\.]\d{5}[\s]\d{5}[\.]\d{6}[\s]\d{5}[\.]\d{6}[\s]\d[\s]\d{14})|(\d{47,48})|(\d{12} \d{12} \d{12} \d{12})
```

## Chave NF-e - Chave de Acesso da Nota Fiscal Eletrônica (44 dígitos)
```
\b\d{44}\b
```

## ISBN - International Standard Book Number
```
(?:ISBN(?:-1[03])?:?\s?)?(?=[0-9X]{10}$|(?=(?:[0-9]+[-\s]){3})[-\s0-9X]{13}$|97[89][0-9]{10}$|(?=(?:[0-9]+[-\s]){4})[-\s0-9]{17}$)(?:97[89][-\s]?)?[0-9]{1,5}[-\s]?[0-9]+[-\s]?[0-9]+[-\s]?[0-9X]
```

## EAN-13 - Código de Barras de Produtos
```
^\d{13}$
```

## Rastreamento Correios (formato completo)
```
\b[A-Za-z]{2}\d{9}[A-Za-z]{2}\b
```

<br>

# Criptomoedas e Wallets <a name="criptomoedas-wallets"></a>

## Bitcoin (BTC)
```
^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$
```

## Ethereum (ETH) e tokens ERC-20 (USDT, USDC)
```
^0x[a-fA-F0-9]{40}$
```

## Tether USDT (TRC-20) - Rede Tron
```
^T[a-zA-Z0-9]{33}$
```

## BNB (Binance Coin)
```
^(bnb1|0x)[a-zA-Z0-9]{38,42}$
```

## Solana (SOL)
```
^[1-9A-HJ-NP-Za-km-z]{32,44}$
```

## XRP (Ripple)
```
^r[a-zA-Z0-9]{24,34}$
```

## Cardano (ADA)
```
^(addr1|stake1)[a-z0-9]{53,}$
```

## Dogecoin (DOGE)
```
^D[5-9A-HJ-NP-U][1-9A-HJ-NP-Za-km-z]{32}$
```

## Litecoin (LTC)
```
^(L|M|ltc1)[a-zA-Z0-9]{26,42}$
```

## Carteiras Multi-chain (detecção genérica)
```
^(0x[a-fA-F0-9]{40}|T[a-zA-Z0-9]{33}|[13][a-zA-Z0-9]{26,35}|bc1[a-z0-9]{39,59})$
```

<br>

# Network e Infraestrutura <a name="network-infraestrutura"></a>

## IPv4
```
(?<![\d.])(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?!\.\d)
```

## IPv6
```
(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))
```

## MAC Address
```
(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})
```

## Domínio Genérico
```
\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b
```

## Domínio + Subdomínio
```
\b(?:[a-zA-Z0-9-]+\.){2,}[a-zA-Z]{2,}\b
```

## Domínio .br (simplificado)
```
\b(?:[a-zA-Z0-9-]+\.)+br\b
```

## Domínio com Porta
```
\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}:\d{1,5}\b
```

## URL Completa
```
\bhttps?:\/\/[^\s\/$.?#].[^\s]*\b
```

## URL com Domínio .br
```
(?:https?:\/\/)?(?:www\.)?[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.br(?:\/[^\s]*)?
```

## URL Encurtada (bit.ly, t.co, tinyurl, etc)
```
\b(?:bit\.ly|t\.co|tinyurl\.com|goo\.gl|ow\.ly|is\.gd|cutt\.ly)\/[a-zA-Z0-9_-]+\b
```

## Microsoft Azure Cloud App
```
\b[a-zA-Z0-9-]+\.cloudapp\.azure\.com\b
```

## Google Cloud (hostname reverso)
```
\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\.bc\.googleusercontent\.com\b
```

## Amazon AWS EC2
```
\bec2-\d{1,3}-\d{1,3}-\d{1,3}-\d{1,3}\.[a-z0-9-]+\.compute\.amazonaws\.com\b
```

## Amazon AWS S3 Bucket
```
\b[a-zA-Z0-9-]+\.s3\.[a-z0-9-]+\.amazonaws\.com\b
```

## Azure Web Apps
```
\b[a-zA-Z0-9-]+\.azurewebsites\.net\b
```

## Heroku
```
\b[a-zA-Z0-9-]+\.herokuapp\.com\b
```

## Vercel
```
\b[a-zA-Z0-9-]+\.vercel\.app\b
```

## Netlify
```
\b[a-zA-Z0-9-]+\.netlify\.app\b
```

## Google Firebase
```
\b[a-zA-Z0-9-]+\.firebaseapp\.com\b
```

<br>

# Tor e Dark Web <a name="tor-darkweb"></a>

## Tor Hidden Service v2 (16 caracteres)
```
\b[a-z2-7]{16}\.onion\b
```

## Tor Hidden Service v3 (56 caracteres)
```
\b[a-z2-7]{56}\.onion\b
```

## Tor .onion (v2 ou v3)
```
\b[a-z2-7]{16,56}\.onion\b
```

<br>

# Cartões de Crédito <a name="cartoes-credito"></a>

## Visa
```
4[0-9]{12}(?:[0-9]{3})?
```

## Mastercard
```
(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}
```

## American Express
```
3[47][0-9]{13}
```

## Elo (Brasil)
```
(?:4011|4312|4389|4514|4576|5041|5066|5067|6277|6362|6363)[0-9]{12}
```

## Hipercard (Brasil)
```
(?:38|60)[0-9]{11,17}
```

## Diners Club
```
3(?:0[0-5]|[68][0-9])[0-9]{11}
```

## Cartão Genérico (múltiplas bandeiras)
```
(?:4[0-9]{12}(?:[0-9]{3})?|(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|6(?:011|5[0-9]{2})[0-9]{12}|(?:2131|1800|35\d{3})\d{11})
```

## Cartão com Separadores (#### #### #### ####)
```
(?:[0-9]{4}[\s-]?){3}[0-9]{4}
```

<br>

# Dados Bancários <a name="dados-bancarios"></a>

Formatos de agência e conta. A regex identifica **o formato**, não o banco: instituições com o mesmo desenho de conta compartilham a mesma expressão.

| Descrição | REGEX |
|---|---|
| Banco do Brasil – Agência 9999-D \| Conta 99999999-D | `\b\d{4}-[0-9X]\s+\d{8}-[0-9X]\b` |
| Bradesco – Agência 9999-D \| Conta 9999999-D | `\b\d{4}-[0-9X]\s+\d{7}-[0-9X]\b` |
| Caixa Econômica – Agência 9999 \| Operação XXX + Conta 99999999-D | `\b\d{4}\s+[0-9]{3}\d{8}-[0-9X]\b` |
| Caixa Econômica – Agência 9999 \| Operação XXXX + Conta 999999999-D (novo formato CP) | `\b\d{4}\s+[0-9]{4}\d{9}-[0-9X]\b` |
| Itaú – Agência 9999 \| Conta 99999-D | `\b\d{4}\s+\d{5}-[0-9X]\b` |
| Sicredi – Agência 9999 \| Conta 999999 | `\b\d{4}\s+\d{6}\b` |
| BS2 – Agência 9999 \| Conta 999999-D | `\b\d{4}\s+\d{6}-[0-9X]\b` |
| Agência 9999 \| Conta 9999999-D – Banco Original, C6, Cora, Next, Stone (formato, não identifica o banco) | `\b\d{4}\s+\d{7}-[0-9X]\b` |
| Agência 9999 \| Conta 99999999-D – Santander, PagSeguro, Safra, Unicred (formato, não identifica o banco) | `\b\d{4}\s+\d{8}-[0-9X]\b` |
| Agência 9999 \| Conta 999999999-D – Inter, Banrisul, Sicoob, BRB, Neon/Votorantim (formato, não identifica o banco) | `\b\d{4}\s+\d{9}-[0-9X]\b` |
| Agência 9999 \| Conta 9999999999-D – Nubank, PJBank (formato, não identifica o banco) | `\b\d{4}\s+\d{10}-[0-9X]\b` |
| Via Credi – Agência 9999 \| Conta 99999999999-D | `\b\d{4}\s+\d{11}-[0-9X]\b` |
| Mercado Pago – Agência 9999 \| Conta 9999999999999-D | `\b\d{4}\s+\d{13}-[0-9X]\b` |

<br>

## Passaporte
```
^[A-Z]{2}\d{6}$
```

## CRM - Conselho Federal de Medicina
```
\b(?:CRM|crm)[\s\/:-]{0,3}[A-Za-z]{2}[\s\/:-]{0,3}\d{4,7}\b|\b\d{4,7}[\s\/-]?(?:CRM|crm)[\s\/-]?[A-Za-z]{2}\b
```

## Telefone
```
(?:\+?55\s?)?(?:\(?\d{2}\)?[\s.-]?)?(?:9\s?)?\d{4}[-.\s]?\d{4}\b
```
## Siglas das UF`s
```
\b(?:AC|AL|AP|AM|BA|CE|DF|ES|GO|MA|MT|MS|MG|PA|PB|PR|PE|PI|RJ|RN|RS|RO|RR|SC|SP|SE|TO|BR)\b
```

## CADASTUR - (Cadastro de Prestadores de Serviços Turísticos)
```
([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[/]?[0-9]{4}[-]?[0-9]{2})
```
## DATA - (dd-mm-yyyy | dd/mm/yyyy)
```
\b(0[1-9]|[12]\d|3[01])[\/.-](0[1-9]|1[0-2])[\/.-](19|20)\d{2}\b
```

## Inscrição Estadual (IE)
Número de inscrição dado às empresas pelo SEFAZ (Secretária da Fazenda) de cada UF. O comprimento pode variar de 8 a 13 dígitos, dependendo da UF. A REGEX abaixo corresponde ao formato utilizado no estado de São Paulo. Para outros estados, verifique o arquivo JSON na raiz deste repositório.
```
^\d{3}.?\d{3}.?\d{3}.?\d{3}$
```


# REGEX Genéricas <a name="regex-genericas"></a>

## Email
```
([\w._%+-]+)(@|\s@\s|\sat\s|\[at\])([\w.-]+)\.([\w]{2,})
```

## Telefone Brasil
```
(?:\+?55\s?)?(?:\(?\d{2}\)?[\s.-]?)?(?:9\s?)?\d{4}[-.\s]?\d{4}\b
```

## Data (dd-mm-yyyy | dd/mm/yyyy)
```
\b(0[1-9]|[12]\d|3[01])[\/.-](0[1-9]|1[0-2])[\/.-](19|20)\d{2}\b
```

## Hora formato 12h
```
\b(0?[1-9]|1[0-2]):[0-5][0-9]\s?[AaPp]\.?[Mm]\.?
```

## Hora formato 24h
```
([01][0-9]|[2][0-3]):([0-5][0-9])
```

## UUID (Universally Unique Identifiers)
```
\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b
```

## Validador de Senha (8-20 dígitos, maiúsculas, minúsculas, números e especiais)
```
(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%&*!+\-]).{8,20}
```

## Latitude e Longitude
```
[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)
```

## Chave PIX
```
([0-9]{14,20})([bB][rR]\.[gG][oO][vV]\.[bB][cC][bB]\.[pP][iI][xX]).*(6304)([0-9a-zA-Z]{4})
```

## Chave PIX Aleatória
```
\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b
```

## Processo CNJ (Conselho Nacional de Justiça)
```
\b\d{7}-?\d{2}\.?\d{4}\.?[1-9]\.?\d{2}\.?\d{4}\b
```

## Número de Endereço (números ou "S/N", "s/n", "S/n", "s/N")
```
^(?:[Ss]\/?[Nn]|\d{1,6})$
```

<br>

# Identificadores Governamentais <a name="identificadores-gov"></a>

Identificadores públicos brasileiros úteis em investigação de fontes abertas. As entradas com rótulo (SIAPE, NB, ISPB, CNES, IBGE) exigem o prefixo textual para evitar falso positivo, já que o número sozinho é apenas uma sequência de dígitos.

| Descrição | REGEX |
|---|---|
| CPF mascarado - formato publicado em portais de transparência e no TSE | `\*{3}\.?\d{3}\.?\d{3}-?\*{2}` |
| OAB - Inscrição na Ordem dos Advogados do Brasil com seccional | `\b(?:OAB\|oab)[\s\/:-]{0,3}[A-Za-z]{2}[\s\/:-]{0,3}\d{2,6}\b\|\b\d{2,6}[\s\/-]?(?:OAB\|oab)[\s\/-]?[A-Za-z]{2}\b` |
| SIAPE - Matrícula de servidor público federal | `\b(?:SIAPE\|siape)[\s.:nº°-]{0,6}\d{7}\b` |
| Currículo Lattes - Identificador CNPq (16 dígitos) | `\b(?:lattes\.cnpq\.br\/\|ID Lattes:?\s*)\d{16}\b` |
| Processo administrativo federal - numeração SEI/NUP | `\b\d{5}\.\d{6}\/\d{4}-\d{2}\b` |
| NB - Número do Benefício do INSS | `\b(?:NB\|benef[ií]cio)[\s.:nº°-]{0,6}\d{3}\.?\d{3}\.?\d{3}-?\d\b` |
| CCIR/INCRA - Código do imóvel rural | `\b\d{3}\.\d{3}\.\d{3}\.\d{3}-\d\b` |
| Registro ANVISA - Medicamento (registro MS) | `\b(?:MS\|M\.S\.)\s?\d{1}\.?\d{4}\.?\d{4}\.?\d{3}-?\d?\b` |
| ISPB - Identificador de instituição financeira no Bacen | `\b(?:ISPB\|ispb)[\s.:-]{0,3}\d{8}\b` |
| CNPJ raiz - 8 dígitos, sem sufixo de filial e sem DV | `\b\d{2}\.\d{3}\.\d{3}\b` |

<br>

# Redes Sociais e Mensageria <a name="redes-sociais"></a>

| Descrição | REGEX |
|---|---|
| WhatsApp - Links com número brasileiro | `(?:whatsapp\.com\/\|wa\.me\/\|api\.whatsapp\.com\/send\?phone=)(?:\+?55)?\s?\(?\d{2}\)?\s?9?\d{4}[-\s]?\d{4}` |
| Telegram - Links e usernames | `(?:t\.me\/\|telegram\.me\/\|telegram\.dog\/)([a-zA-Z0-9_]{5,32})` |
| Instagram - Perfis | `instagram\.com\/(?!p\/\|reel\/\|reels\/\|stories\/\|explore\/\|tv\/)([A-Za-z0-9_.]{1,30})` |
| Twitter/X - Perfis | `(?:twitter\.com\|x\.com)\/(?!status\/\|i\/\|search\|hashtag\/\|home)([A-Za-z0-9_]{1,15})` |
| Facebook - Perfis | `(?:facebook\.com\/\|fb\.com\/)([a-zA-Z0-9\.]{5,})` |
| LinkedIn - Perfis | `(?:linkedin\.com\/in\/)([a-zA-Z0-9\-]{3,100})` |
| TikTok - Perfis | `(?:tiktok\.com\/@)([a-zA-Z0-9_\.]{2,24})` |
| YouTube - Canais e usuários | `(?:youtube\.com\/(?:@\|c\/\|user\/\|channel\/)\|youtu\.be\/)([A-Za-z0-9_-]{1,})` |
| WhatsApp - Convite de grupo | `chat\.whatsapp\.com\/(?:invite\/)?[A-Za-z0-9]{20,24}` |
| Telegram - Convite de canal ou grupo privado | `t\.me\/(?:joinchat\/\|\+)[A-Za-z0-9_-]{16,}` |
| Discord - Convite de servidor | `(?:discord\.gg\|discord(?:app)?\.com\/invite)\/[A-Za-z0-9-]{2,32}` |
| GitHub - Perfis e organizações | `github\.com\/(?!orgs\/\|topics\/\|search\|features\/)([A-Za-z0-9-]{1,39})\b` |
| Reddit - Perfis | `reddit\.com\/(?:user\|u)\/([A-Za-z0-9_-]{3,20})` |
| Bluesky - Perfis | `bsky\.app\/profile\/([A-Za-z0-9.-]{3,253})` |
| Threads - Perfis | `threads\.(?:net\|com)\/@([A-Za-z0-9_.]{1,30})` |
| Twitch - Canais | `twitch\.tv\/(?!videos\/\|directory\/)([A-Za-z0-9_]{4,25})` |
| Kwai - Perfis | `(?:kwai\.com\|kwai-video\.com)\/@?([A-Za-z0-9_.-]{3,30})` |

<br>

# Geolocalização <a name="geolocalizacao"></a>

| Descrição | REGEX |
|---|---|
| Coordenadas GPS (latitude, longitude) - formato decimal | `[-+]?([1-8]?\d(\.\d+)?\|90(\.0+)?),\s*[-+]?(180(\.0+)?\|((1[0-7]\d)\|([1-9]?\d))(\.\d+)?)` |
| Google Plus Code (Open Location Code) | `\b[23456789CFGHJMPQRVWX]{4,8}\+[23456789CFGHJMPQRVWX]{2,3}\b` |
| Coordenadas em graus, minutos e segundos (DMS) | `\d{1,3}[°º]\s?\d{1,2}['′]\s?\d{1,2}(?:[.,]\d+)?[\"″]?\s?[NSLWEO]` |

<br>

# Veículos, Negócios e Educação <a name="veiculos-negocios-educacao"></a>

| Descrição | REGEX |
|---|---|
| Chassis (VIN) - Número de identificação do veículo (17 caracteres) | `^[A-HJ-NPR-Z0-9]{17}$` |
| ANTT - Registro de transportador | `\b\d{8}\b` |
| SUFRAMA - Superintendência da Zona Franca de Manaus | `\d{2}\.\d{3}\.\d{3}\/\d{4}` |
| CAGED - Cadastro Geral de Empregados e Desempregados (precedido do rótulo) | `(?:CAGED\|caged)[\s.:nº°-]{0,6}(\d{7})\b` |
| CAEPF - Cadastro de Atividade Econômica da Pessoa Física | `\d{3}\.\d{3}\.\d{3}\-\d{2}\/\d{2}` |
| ENEM - Número de inscrição (12 dígitos) | `\d{12}` |
| Registro Profissional - CREA, CRO, CRC, COREN, etc | `\b(CR[A-Z]{1,3})\s?\d{4,10}[\/\-]?[A-Z]{2}\b` |

<br>

# Documentos Complementares <a name="documentos-complementares"></a>

| Descrição | REGEX |
|---|---|
| NIS - Número de Identificação Social | `\b\d{3}\.\d{5}\.\d{2}-\d{1}\b` |
| Certidão (Nascimento/Casamento) - Formato nacional unificado | `\d{6}\s\d{2}\s\d{2}\s\d{4}\s\d{1}\s\d{5}\s\d{3}\s\d{7}-\d{2}` |

<br>

# Financeiro Internacional <a name="financeiro-internacional"></a>

| Descrição | REGEX |
|---|---|
| SWIFT/BIC - Código para transferências internacionais | `^[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?$` |
| IBAN - International Bank Account Number | `^[A-Z]{2}\d{2}[A-Z0-9]{1,30}$` |

<br>

# Hashes e Tokens <a name="hashes-tokens"></a>

| Descrição | REGEX |
|---|---|
| Hash MD5 - 32 caracteres hexadecimais | `\b[a-fA-F0-9]{32}\b` |
| Hash SHA-1 - 40 caracteres hexadecimais | `\b[a-fA-F0-9]{40}\b` |
| Hash SHA-256 - 64 caracteres hexadecimais | `\b[a-fA-F0-9]{64}\b` |
| JWT Token - JSON Web Token | `eyJ[A-Za-z0-9\-_=]+\.eyJ[A-Za-z0-9\-_=]+\.[A-Za-z0-9\-_.+\/=]*` |
| Hash bcrypt | `\$2[aby]?\$\d{2}\$[.\/A-Za-z0-9]{53}` |
| Hash SHA-512 - 128 caracteres hexadecimais | `\b[a-fA-F0-9]{128}\b` |

<br>

# Credenciais de API e Segredos <a name="credenciais-api"></a>

Padrões para varredura de segredos expostos em código, logs e dumps. Inclui gateways de pagamento brasileiros (Mercado Pago, Pagar.me, Asaas).

| Descrição | REGEX |
|---|---|
| AWS Access Key ID | `(?:A3T[A-Z0-9]\|AKIA\|AGPA\|AIDA\|AROA\|AIPA\|ANPA\|ANVA\|ASIA)[A-Z0-9]{16}` |
| AWS Secret Access Key | `(?i)aws(.{0,20})?['"][0-9a-zA-Z\/+]{40}['"]` |
| Google API Key | `AIza[0-9A-Za-z\-_]{35}` |
| Google Captcha Key | `6L[0-9A-Za-z\-_]{38}\|^6[0-9a-zA-Z_-]{39}$` |
| Google OAuth Token | `ya29\.[0-9A-Za-z\-_]+` |
| Firebase Secret | `AAAA[A-Za-z0-9_-]{7}:[A-Za-z0-9_-]{140}` |
| GitHub Personal Access Token | `ghp_[0-9a-zA-Z]{36}` |
| GitHub Fine-Grained Token | `github_pat_[0-9a-zA-Z_]{20,}` |
| GitHub OAuth Access Token | `gho_[0-9a-zA-Z]{36}` |
| GitHub OAuth App Secret | `(?i)(?:github\|gh)(?:.{0,20})?['\"][a-f0-9]{40}['\"]` |
| GitLab Personal Access Token | `glpat-[0-9a-zA-Z\-_]{20}` |
| GitLab Runner Token | `glrt-[a-zA-Z0-9_\-]{20}` |
| Slack Token | `xox[baprs]-([0-9a-zA-Z]{10,48})?` |
| Stripe Secret Key (Live) | `sk_live_[0-9a-zA-Z]{24}` |
| Stripe Publishable Key (Live) | `pk_live_[0-9a-zA-Z]{24}` |
| Stripe Secret Key (Test) | `sk_test_[0-9a-zA-Z]{24}` |
| Stripe Restricted Key | `rk_live_[0-9a-zA-Z]{24}` |
| Twilio API Key | `SK[0-9a-fA-F]{32}` |
| Twilio Account SID | `AC[a-zA-Z0-9_\-]{32}` |
| Telegram Bot Token | `\d{9}:[a-zA-Z0-9_\-]{35}` |
| SendGrid API Key | `SG\.[\w\d\-_]{22}\.[\w\d\-_]{43}` |
| Mailgun API Key | `key-[0-9a-zA-Z]{32}` |
| Dropbox Access Token | `sl\.[A-Za-z0-9_\-]{20,100}` |
| Shopify Access Token | `shpat_[0-9a-fA-F]{32}` |
| Shopify Shared Secret | `shpss_[0-9a-fA-F]{32}` |
| Facebook Access Token | `EAACEdEose0cBA[0-9A-Za-z]+` |
| Heroku API Key | `[hH]eroku['"][0-9a-f]{32}['"]` |
| DigitalOcean Token | `dop_v1_[a-z0-9]{64}` |
| Asana Personal Access Token | `0\/[0-9a-z]{32}` |
| Linear API Key | `lin_api_[a-zA-Z0-9]{40}` |
| OAuth Client Secret | `(?i)client_secret['"]\s*[:=]\s*['"][a-zA-Z0-9\-_.~]{10,100}['"]` |
| OAuth Client ID | `(?i)client_id['"]\s*[:=]\s*['"][a-zA-Z0-9\-_.~]{10,100}['"]` |
| Azure Client Secret | `(?i)azure(.{0,20})?client.secret(.{0,20})?['"][a-zA-Z0-9._%+-]{32,}['"]` |
| Microsoft Teams Webhook | `https:\/\/[a-z]+\.webhook\.office\.com\/webhookb2\/[a-zA-Z0-9@\-]+\/.*` |
| Authorization Bearer Token | `Bearer\s+[a-zA-Z0-9\-._~+\/]+=*` |
| CircleCI Token | `circle-token=[a-z0-9]{40}` |
| Travis CI Token | `(?i)travis(.{0,20})?token['"]\s*[:=]\s*['"][a-z0-9]{30,}['"]` |
| Jenkins Crumb Token | `Jenkins-Crumb:\s*[a-z0-9]{30,}` |
| Azure DevOps Token | `(?i)(?:azure\|devops\|vsts)(?:.{0,20})?['\"][a-z0-9]{52}['\"]` |
| Bitbucket OAuth Key | `(?i)bitbucket(.{0,20})?key['"]\s*[:=]\s*['"][a-zA-Z0-9]{20,}['"]` |
| Bitbucket OAuth Secret | `(?i)bitbucket(.{0,20})?secret['"]\s*[:=]\s*['"][a-zA-Z0-9]{20,}['"]` |
| Netlify Access Token | `netlifyAuthToken\s*=\s*['"][a-z0-9]{40}['"]` |
| Bugsnag API Key | `(?i)bugsnag(?:.{0,20})?['\"][a-f0-9]{32}['\"]` |
| Datadog API Key | `(?i)datadog(?:.{0,20})?['\"][a-z0-9]{32}['\"]` |
| Loggly Token | `[a-z0-9]{30}-[a-z0-9]{10}` |
| New Relic Key | `NRII-[a-zA-Z0-9]{20,}` |
| Mixpanel Token | `(?i)mixpanel(.{0,20})?token['"]\s*[:=]\s*['"][a-z0-9]{32}['"]` |
| Heap Analytics App ID | `heapSettings\.appId\s*=\s*['"][a-z0-9]{8,12}['"]` |
| Keen IO Project ID | `projectId['"]?\s*:\s*['"][a-f0-9]{24}['"]` |
| Keen IO Write Key | `writeKey['"]?\s*:\s*['"][a-zA-Z0-9]{64}['"]` |
| Snyk Token | `snyk_token\s*=\s*[a-f0-9\-]{36}` |
| Rollbar Access Token | `access_token['"]?\s*:\s*['"][a-z0-9]{32}['"]` |
| Twitch API Key | `(?i)twitch(.{0,20})?key['"]\s*[:=]\s*['"][a-zA-Z0-9]{20,}['"]` |
| Discord Bot Token | `[MN][A-Za-z\d]{23}\.[\w\-]{6}\.[\w\-]{27}` |
| Discord Webhook URL | `https:\/\/discord(?:app)?\.com\/api\/webhooks\/[0-9]+\/[a-zA-Z0-9_\-]+` |
| Steam Web API Key | `(?i)steam(.{0,20})?key['"]\s*[:=]\s*['"][a-zA-Z0-9]{32}['"]` |
| Riot Games API Key | `RGAPI-[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}` |
| Algolia API Key | `(?i)(algolia\|application)_?key['"]\s*[:=]\s*['"][a-zA-Z0-9]{10,}['"]` |
| Firebase API Key (Config) | `firebaseConfig\s*=\s*{[^}]*apiKey\s*:\s*['"][^'"]+['"]` |
| Cloudinary URL | `cloudinary:\/\/[0-9]{15}:[a-zA-Z0-9]+@[a-zA-Z]+` |
| Sentry DSN | `https:\/\/[a-zA-Z0-9]+@[a-z]+\.ingest\.sentry\.io\/\d+` |
| Segment API Key | `(?i)segment(.{0,20})?key['"]\s*[:=]\s*['"][a-zA-Z0-9]{10,}['"]` |
| Intercom Access Token | `(?i)intercom(.{0,20})?token['"]\s*[:=]\s*['"][a-zA-Z0-9\-_]{20,}['"]` |
| Amplitude API Key | `apiKey['"]?\s*:\s*['"][a-z0-9\-]{32,64}['"]` |
| Plaid Client Secret | `plaid(.{0,20})?(client)?secret['"]\s*[:=]\s*['"][a-z0-9\-_]{30,}['"]` |
| AWS MWS Token | `amzn\.mws\.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}` |
| OpenAI API Key | `\bsk-(?:proj-)?[A-Za-z0-9_-]{32,}\b` |
| Anthropic API Key | `\bsk-ant-api03-[A-Za-z0-9_-]{80,}\b` |
| Hugging Face Token | `\bhf_[A-Za-z0-9]{34}\b` |
| npm Access Token | `\bnpm_[A-Za-z0-9]{36}\b` |
| Slack Webhook URL | `https:\/\/hooks\.slack\.com\/services\/T[A-Za-z0-9_]+\/B[A-Za-z0-9_]+\/[A-Za-z0-9]{24}` |
| Google Service Account (JSON) | `\"type\"\s*:\s*\"service_account\"` |
| Grafana Service Account Token | `\bglsa_[A-Za-z0-9]{32}_[A-Fa-f0-9]{8}\b` |
| Databricks Token | `\bdapi[a-f0-9]{32}\b` |
| Mercado Pago Access Token | `\bAPP_USR-\d{16,}-\d{6}-[a-f0-9]{32}-\d{6,}\b` |
| Pagar.me API Key | `\b(?:ak\|sk)_(?:live\|test)_[A-Za-z0-9]{30,}\b` |
| Asaas API Key | `\$aact_[A-Za-z0-9_=\-]{80,}` |

<br>

# Bancos de Dados e Containers <a name="bancos-containers"></a>

| Descrição | REGEX |
|---|---|
| MongoDB Connection URI | `mongodb(\+srv)?:\/\/[^\s'"]+` |
| PostgreSQL URI | `postgres(ql)?:\/\/[^\s'"]+` |
| MySQL URI | `mysql:\/\/[^\s'"]+` |
| Redis URI | `redis:\/\/[^\s'"]+` |
| Elasticsearch URI | `elasticsearch:\/\/[^\s'"]+` |
| Supabase DB Key | `supabase\.co\/[a-z0-9]{15,}` |
| Firebase URL | `https:\/\/[a-z0-9\-]+\.firebaseio\.com` |
| JDBC URL | `jdbc:\w+:\/\/[^\s'"]+` |
| AWS RDS Hostname | `[a-z0-9\-]+\.rds\.amazonaws\.com` |
| Cloud SQL URI (GCP) | `googleapis\.com\/sql\/v1beta4\/projects\/` |
| Docker Hub Password | `(?i)docker(.{0,20})?password['"]\s*[:=]\s*['"][^\s'"]{8,}['"]` |
| AWS IAM Role ARN | `arn:aws:iam::[0-9]{12}:role\/[A-Za-z0-9_+=,.@\-_\/]+` |
| AWS S3 Bucket URL | `s3:\/\/[a-z0-9\-\.]{3,63}` |
| Kubernetes Secret Name | `(?i)secretName:\s*['"]?[a-z0-9\-]+['"]?` |
| Helm Secret Value | `(?i)secret\s*:\s*['"][^'"]+['"]` |
| GitHub Actions Secret Reference | `\$\{\{\s*secrets\.[A-Z0-9_]+\s*\}\}` |
| GitHub Actions Encrypted Value | `encrypted_value:\s*['"][a-zA-Z0-9+\/=]{10,}['"]` |
| K8s Service Account Token | `eyJhbGciOiJSUzI1NiIsImtpZCI6` |
| Vault Token | `(?i)vault(?:.{0,20})?['\"]s\.[a-zA-Z0-9]{24,}['\"]` |
| Hashicorp Vault URL | `https:\/\/vault\.[a-z0-9\-_\.]+\.com` |

<br>

# Chaves Privadas e Certificados <a name="chaves-privadas"></a>

| Descrição | REGEX |
|---|---|
| RSA Private Key | `-----BEGIN RSA PRIVATE KEY-----` |
| DSA Private Key | `-----BEGIN DSA PRIVATE KEY-----` |
| EC Private Key | `-----BEGIN EC PRIVATE KEY-----` |
| OpenSSH Private Key | `-----BEGIN OPENSSH PRIVATE KEY-----` |
| PGP Private Key Block | `-----BEGIN PGP PRIVATE KEY BLOCK-----` |
| PEM Certificate | `-----BEGIN CERTIFICATE-----` |

<br>

# Padrões Sensíveis e URLs Internas <a name="padroes-sensiveis"></a>

| Descrição | REGEX |
|---|---|
| Password Assignment | `(?i)(password\|passwd\|pwd)['"]\s*[:=]\s*['"][^'"]{4,}['"]` |
| API Key in Variable | `(?i)(api[_\-]?key)['"]\s*[:=]\s*['"][a-zA-Z0-9\-_.]{8,100}['"]` |
| Secret in Variable | `(?i)(secret\|token)['"]\s*[:=]\s*['"][a-zA-Z0-9\-_.]{8,100}['"]` |
| Basic Auth String | `(?i)(username\|user\|email)['"]\s*[:=]\s*['"][^\s'"@]{1,100}['"].*?(password\|pwd)['"]\s*[:=]\s*['"][^\s'"]{4,100}['"]` |
| Base64 High Entropy String | `['"][A-Za-z0-9+\/]{40,}={0,2}['"]` |
| Session ID | `(?i)sessionid['"]\s*[:=]\s*['"][a-zA-Z0-9]{10,}['"]` |
| Cookie Name Generic | `(?i)set-cookie:\s*[a-zA-Z0-9_\-]+=` |
| CSRF Token | `(?i)csrf(token)?['"]\s*[:=]\s*['"][a-zA-Z0-9\-_]{8,}['"]` |
| JWT in Local Storage | `localStorage\.setItem\(['"]token['"],\s*['"]eyJ[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+['"]\)` |
| Private IP (Internal) | `\b(10\.\d{1,3}\|\b192\.168\|\b172\.(1[6-9]\|2\d\|3[01]))\.\d{1,3}\.\d{1,3}` |
| Localhost Reference | `localhost:[0-9]{2,5}` |
| Dev/Stage URL | `(dev\|staging\|test)\.[a-z0-9.\-]+\.(com\|net\|io)` |
| Internal Subdomain URL | `https?:\/\/[a-z0-9.\-]+\.internal\.[a-z]{2,}` |
| Preprod URLs | `https:\/\/preprod\.[a-z0-9\-]+\.[a-z]{2,}` |

<br>


<br>

---

## 📄 LICENÇA

Este projeto está licenciado sob: veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 AUTOR

**MrCl0wn**
- 🌐 **Blog**: [http://blog.mrcl0wn.com](http://blog.mrcl0wn.com)
- 🐙 **GitHub**: [@MrCl0wnLab](https://github.com/MrCl0wnLab)
- 🐦 **Twitter**: [@MrCl0wnLab](https://twitter.com/MrCl0wnLab)
- 📧 **Email**: mrcl0wnlab\@\gmail.com

---

## Contribuições ✨ <a name="contributing"></a>

Contribuições de qualquer tipo são bem-vindas!

<a href="https://github.com/osintbrazuca/osint-brazuca-regex/graphs/contributors">
  <img src="https://contributors-img.web.app/image?repo=osintbrazuca/osint-brazuca-regex&max=500" alt="Lista de colaboradores" width="100%"/>
</a>
    
---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela!**

**💡 Sugestões e feedback são sempre bem-vindos!**

**💀 Hacker Hackeia!**

</div>
