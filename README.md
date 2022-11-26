<h1 align="center">
  <br>
  <a href="https://nuclei.projectdiscovery.io"><img src="assets/logo_profile.png" width="300px" alt="OSINT Brazuca"></a>
</h1>

<h4 align="center">OSINT (Open-source intelligence) / <b>REGEX</b></h4>


<p align="center">
<a href="https://github.com/osintbrazuca/osint-brazuca-regex/blob/main/LICENSE"><img src="https://img.shields.io/github/license/osintbrazuca/osint-brazuca-regex?color=blue"></a>
<a href="https://github.com/osintbrazuca/osint-brazuca/graphs/contributors"><img src="https://img.shields.io/github/contributors-anon/osintbrazuca/osint-brazuca-regex"></a>
<a href="https://github.com/osintbrazuca/osint-brazuca-regex/issues"><img src="https://img.shields.io/github/issues-raw/osintbrazuca/osint-brazuca-regex"></a>
<a href="https://github.com/osintbrazuca/osint-brazuca-regex/discussions"><img src="https://img.shields.io/github/discussions/osintbrazuca/osint-brazuca-regex"></a>
<a href="https://github.com/osintbrazuca/osint-brazuca-regex/network/members"><img src="https://img.shields.io/github/forks/osintbrazuca/osint-brazuca-regex"></a>
<img src="https://img.shields.io/github/stars/osintbrazuca/osint-brazuca-regex.svg?style=social" title="Stars" /> 
</p>


# Introdução
**OSINT Brazuca Regex** é um repositório criado com intuito de reunir **expressões regulares** dentro do contexto Brasil 🇧🇷.

<br>


# Documentos Brasileiros

## CNPJ - Cadastro Nacional da Pessoa Jurídica
```
^(\d{2}.?\d{3}.?\d{3}\/?\d{4}\-?\d{2})$
```

## CPF - Cadastro de Pessoas Físicas
```
^\d{3}.?\d{3}.?\d{3}\-?\d{2}$
```
### CPF - Cadastro de Pessoas Físicas por Localidade
<details>
  <summary>Rio Grande do Sul</summary>
  <br>
  Dígito <b>0</b>
  <p>Ex: 999.999.99<ins>0</ins>-99</p>
  <pre>^\d{3}.?\d{3}.?\d{2}[0]{1}\-?\d{2}$</pre>
  <br>
</details>
<details>
  <summary>Distrito Federal, Goiás, Mato Grosso, Mato Grosso do Sul e Tocantins</summary>
  <br>
  Dígito <b>1</b>
  <p>Ex: 000.000.00<ins>1</ins>-00</p>
  <pre>^\d{3}.?\d{3}.?\d{2}[1]{1}\-?\d{2}$</pre>
  <br>
</details>
<details>
  <summary>Amazonas, Pará, Roraima, Amapá, Acre e Rondônia</summary>
  <br>
  Dígito <b>2</b>
  <p>Ex: 000.000.00<ins>2</ins>-00</p>
  <pre>^\d{3}.?\d{3}.?\d{2}[2]{1}\-?\d{2}$</pre>
  <br>
</details>
<details>
  <summary>Ceará, Maranhão e Piauí</summary>
  <br>
  Dígito <b>3</b>
  <p>Ex: 000.000.00<ins>3</ins>-00</p>
  <pre>^\d{3}.?\d{3}.?\d{2}[3]{1}\-?\d{2}$</pre>
  <br>
</details>
<details>
  <summary>Paraíba, Pernambuco, Alagoas e Rio Grande do Norte</summary>
  <br>
  Dígito <b>4</b>
  <p>Ex: 000.000.00<ins>4</ins>-00</p>
  <pre>^\d{3}.?\d{3}.?\d{2}[4]{1}\-?\d{2}$</pre>
  <br>
</details>
<details>
  <summary>Bahia e Sergipe</summary>
  <br>
  Dígito <b>5</b>
  <p>Ex: 000.000.00<ins>5</ins>-00</p>
  <pre>^\d{3}.?\d{3}.?\d{2}[5]{1}\-?\d{2}$</pre>
  <br>
</details>
<details>
  <summary>Minas Gerais</summary>
  <br>
  Dígito <b>6</b>
  <p>Ex: 000.000.00<ins>6</ins>-00</p>
  <pre>^\d{3}.?\d{3}.?\d{2}[6]{1}\-?\d{2}$</pre>
  <br>
</details>
<details>
  <summary>Rio de Janeiro e Espírito Santo</summary>
  <br>
  Dígito <b>7</b>
  <p>Ex: 000.000.00<ins>7</ins>-00</p>
  <pre>^\d{3}.?\d{3}.?\d{2}[7]{1}\-?\d{2}$</pre>
  <br>
</details>
<details>
  <summary>São Paulo</summary>
  <br>
  Dígito <b>8</b>
  <p>Ex: 000.000.00<ins>8</ins>-00</p>
  <pre>^\d{3}.?\d{3}.?\d{2}[8]{1}\-?\d{2}$</pre>
  <br>
</details>
<details>
  <summary>Paraná e Santa Catarina</summary>
  <br>
  Dígito <b>9</b>
  <p>Ex: 000.000.00<ins>9</ins>-00</p>
  <pre>^\d{3}.?\d{3}.?\d{2}[9]{1}\-?\d{2}$</pre>
  <br>
</details>



## RG - Registro Geral 
```
(\d{1,2}\.?)(\d{3}\.?)(\d{3})(\-?[0-9Xx]{1})
```

## CNH - Carteira Nacional de Habilitação
```
((cnh.*[0-9]{11})|(CNH.*[0-9]{11})|(habilitação.*[0-9]{11})|(carteira.*[0-9]{11}))
```

## CEP - Código de Endereçamento Postal 
```
(^\d{5})\-?(\d{3}$)
```

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
^([a-zA-Z]{3}\d[a-jA-J]\d{2})|([a-zA-Z]{3}-\d{4})$
```

## Boleto Bancário e Linha Digitável
```
(\d{5}[\.]\d{5}[\s]\d{5}[\.]\d{6}[\s]\d{5}[\.]\d{6}[\s]\d[\s]\d{14})|(\d{47,48})|(\d{12} \d{12} \d{12} \d{12})
```

## Chave PIX Aleatória
```
([a-z\d]{8})\-([a-z\d]{4})\-([a-z\d]{4})\-([a-z\d]{4})\-([a-z\d]{12})
```

## Passaporte
```
^[A-Z]{2}\d{6}$
```

## CRM - Conselho Federal de Medicina
```
([0-9-\/]{5,11})(?i)[a-z]{2}
```

## Telefone
```
(?:(?:\+|00)?(55)\s?)?(?:\(?([1-9][0-9])\)?\s?)(?:((?:9\d|[2-9])\d{3})\-?(\d{4}))
```
## Siglas das UF`s
```
(AC|AL|AP|AM|BA|CE|DF|ES|GO|MA|MT|MS|MG|PA|PB|PR|PE|PI|RJ|RN|RS|RO|RR|SC|SP|SE|TO|BR)
```

## CADASTUR - (Cadastro de Prestadores de Serviços Turísticos)
```
([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})
```
## DATA - (dd-mm-yyyy | dd/mm/yyyy)
```
(0[1-9]|1[0-9]|2[0-9]|3[0-1])[- | \/](0[1-9]|1[0-2])[- | \/]([0-9]{4})
```

<br>

# REGEX Genéricas


## Bitcoin

```
^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$
```

## URL

```
https?:\/\/(www\.)?[^\/]*?\/?([^$]*?$)?
```


## Email

```
[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+
```

## IP

```
[[:digit:]]{1,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,3}
```

## IPv6

```
(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))
```

## Mac Address

```
(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})
```

## Hora formato 12h

```
((0?[1-9]|1[0-2]):([0-5][0-9].?([a].?[m].?|[p].?[m].?)?))
```

## Hora formato 24h

```
([01][0-9]|[2][0-3]):([0-5][0-9])
```

## Senha (8-20 dígitos, letras maiúsculas, minúsculas, números e caracteres especiais)

```
^(?=.*[A-Z])(?=.*[a-z])(?=.*[\d])(?=.*[@#$%&*!-+&*]).{8,20}$
```

## Latitude e Longitude

```
(\+|-)?(?:180(?:(?:\.0{1,6})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,6})?))
```

<br>

# Autores 👔 <a name="autores"></a>
<p >
<img src="assets/logo_profile.png" width="20%" /><br>
<p>

- **Cleiton P. (a.k.a. MrCl0wnLab)** - [Twitter](https://twitter.com/MrCl0wnLab), [Git](https://github.com/MrCl0wnLab)

- **Diego (a.k.a. c4nh0t0)** - [Twitter](https://twitter.com/C4nh0t0GH), [Git](https://github.com/c4nh0t0)

---

## Contribuições ✨ <a name="contribuicoes"></a>
Contribuições de qualquer tipo são bem-vindas!
    
---
    
## Créditos 👏 <a name="creditos"></a>
A todas as instituições públicas governamentais e iniciativas privadas que disponibilizaram os links para consulta.
<br>
A todos que de alguma forma contribuíram para o compartilhamento de links e tricks de consulta nos websites.
