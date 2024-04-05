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

### CEP - Código de Endereçamento Postal por localidade

  * Centro-Oeste
    <details>
      <summary>Distrito Federal</summary>
      <br>
      70000-000 a 72799-999 e 73000-000 a 73699-999
      <pre>(7([0-2][0-7]|3[0-6])\d{2}-\d{3})</pre>
      <br>
    </details>
    <details>
      <summary>Goiás</summary>
      <br>
      72800-000 a 72999-999 e 73700-000 a 76799-999
      <pre>(7(2[8-9]|[3-6]7)\d{2}-\d{3})</pre>
      <br>
    </details>
    <details>
      <summary>Mato Grosso do Sul</summary>
      <br>
      79000-000 a 79999-999
      <pre>(79\d{3}-\d{3})</pre>
      <br>
    </details>
    <details>
      <summary>Mato Grosso</summary>
      <br>
      78000-000 a 78899-999
      <pre>(78[0-8]\d{2}-\d{3})</pre>
      <br>
    </details>

  * Nordeste

    <details>
      <summary>Alagoas</summary>
      <br>
      57000-000 a 57999-999
      <pre>(57\d{3}-\d{3})</pre>
      <br>
    </details>
    <details>
      <summary>Bahia</summary>
      <br>
      40000-000 a 48999-999
      <pre>(4[0-8]\d{3}-\d{3})</pre>
      <br>
    </details>
    <details>
      <summary>Ceará</summary>
      <br>
      60000-000 a 63999-999
      <pre>(6[0-3]\d{3}-\d{3})</pre>
      <br>
    </details>
      <details>
      <summary>Maranhão</summary>
      <br>
      65000-000 a 65999-999
      <pre>(65\d{3}-\d{3})</pre>
      <br>
    </details>
    <details>
      <summary>Paraíba</summary>
      <br>
      58000-000 a 58999-999
      <pre>(58\d{3}-\d{3})</pre>
      <br>
    </details>
    <details>
      <summary>Pernambuco</summary>
      <br>
      50000-000 a 56999-999
      <pre>(5[0-6]\d{3}-\d{3})</pre>
      <br>
    </details>
    <details>
      <summary>Piauí</summary>
      <br>
      64000-000 a 64999-999
      <pre>(64\d{3}-\d{3})</pre>
      <br>
    </details>
    <details>
      <summary>Rio Grande do Norte</summary>
      <br>
      59000-000 a 59999-999
      <pre>(59\d{3}-\d{3})</pre>
      <br>
    </details>
    <details>
      <summary>Sergipe</summary>
      <br>
      49000-000 a 49999-999
      <pre>(49\d{3}-\d{3})</pre>
      <br>
    </details>

  * Norte
    <details>
      <summary>Acre</summary>
      <br>
      69900-000 a 69999-999
      <pre>(699\d{2}-\d{3})</pre>
      <br>
    </details>
    <details>
      <summary>Amapá</summary>
      <br>
      68900-000 a 68999-999
      <pre>(689\d{2}-\d{3})</pre>
      <br>
    </details>
    <details>
      <summary>Amazonas</summary>
      <br>
      69000-000 a 69299-999 e 69400-000 a 69899-999
      <pre>(69([0-2]|[4-8])\d{2}-\d{3})</pre>
      <br>
    </details>
    <details>
      <summary>Pará</summary>
      <br>
      66000-000 a 68899-999
      <pre>(6[6-8][0-8]\d{2}-\d{3})</pre>
      <br>
    </details>
    <details>
      <summary>Rondônia</summary>
      <br>
      76800-000 a 76999-999
      <pre>(76[8-9]\d{2}-\d{3})</pre>
      <br>
    </details>
    <details>
      <summary>Roraima</summary>
      <br>
      69300-000 a 69399-999
      <pre>(693\d{2}-\d{3})</pre>
      <br>
    </details>
    <details>
      <summary>Tocantins</summary>
      <br>
      77000-000 a 77999-999
      <pre>(77\d{3}-\d{3})</pre>
      <br>
    </details>

  * Sudeste
    <details>
      <summary>Espírito Santo</summary>
      <br>
      29000-000 a 29999-999
      <pre>(29\d{3}-\d{3})</pre>
      <br>
    </details>
    <details>
      <summary>Minas Gerais</summary>
      <br>
      30000-000 a 39999-999
      <pre>(3\d{4}-\d{3})</pre>
      <br>
    </details>
    <details>
      <summary>Rio de Janeiro</summary>
      <br>
      20000-000 a 28999-999
      <pre>(2[0-8]\d{3}-\d{3})</pre>
      <br>
    </details>
    <details>
      <summary>São Paulo</summary>
      <br>
      01000-000 a 19999-999
      <pre>([0-1][1-9]\d{3}-\d{3})</pre>
      <br>
    </details>

  * Sul
    <details>
      <summary>Paraná</summary>
      <br>
      80000-000 a 87999-999
      <pre>(8[0-7]\d{3}-\d{3})</pre>
      <br>
    </details>
    <details>
      <summary>Rio Grande do Sul</summary>
      <br>
      90000-000 a 99999-999
      <pre>(9\d{4}-\d{3})</pre>
      <br>
    </details>
    <details>
      <summary>Santa Catarina</summary>
      <br>
      88000-000 a 89999-999
      <pre>(8[8-9]\d{3}-\d{3})</pre>
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
^([a-zA-Z]{3}\d[a-jA-J]\d{2})|([a-zA-Z]{3}-\d{4})$
```

## Boleto Bancário e Linha Digitável
```
(\d{5}[\.]\d{5}[\s]\d{5}[\.]\d{6}[\s]\d{5}[\.]\d{6}[\s]\d[\s]\d{14})|(\d{47,48})|(\d{12} \d{12} \d{12} \d{12})
```

## Chave PIX 
```
([0-9]{14})(br.gov.bcb.(|-)pix).*(6304)([0-9a-zA-Z]{4})
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

## Inscrição Estadual (IE)
Número de inscrição dado às empresas pelo SEFAZ (Secretária da Fazenda) de cada UF. O comprimento pode variar de 8 a 13 dígitos, dependendo da UF. A REGEX abaixo corresponde ao formato utilizado no estado de São Paulo. Para outros estados, verifique o arquivo JSON na raiz deste repositório.
```
^\d{3}.?\d{3}.?\d{3}.?\d{3}$
```

<br>

# REGEX Genéricas


## Bitcoin

```
^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$
```

## URL

```
https?:\\/\\/(www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b([-a-zA-Z0-9()!@:%_\\+.~#?&\\/\\/=]*)
```


## Email

```
([\w._%+-]+)(@|\s@\s|\sat\s|\[at\])([\w.-]+)\.([\w]{2,})
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

## UUID
```
(^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-4[a-fA-F0-9]{3}-[8|9|aA|bB][a-fA-F0-9]{3}-[a-fA-F0-9]{12}$)
```

## Número de Endereço (números ou "S/N", "s/n", "S/n", "s/N")
```
^(?:s\/n|S\/n|S\/N|s\/N)|^(\d)*$
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
