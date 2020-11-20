# Cashback

Uma Rest API (desenvolvida com o Framework Python Django), para revendedores cadastrarem suas compras e acompanhar o retorno de cashback.

O Projeto conta com:

- [x] Banco de dados relacional
- [x] Logs
- [x] Teste unitário
- [x] Autenticação JWT
- [ ] Teste de integração

## Requerimentos

Este projeto requer:

- Python 3.8.6
- Poetry

## Instalando as dependências

Este projeto utiliza o [Poetry](https://python-poetry.org/) como gerenciador de dependências, Veja as [Instruções de instalação](https://python-poetry.org/docs/#installation) e instale de acordo com o seu sistema operacional.

Com o Poetry devidamente instalado, instale as dependências do projeto executando o comando:
```shell script
$ poetry install
```

O Poetry irá criar uma `virtualenv` e instalar as todas as dependências.
Após a instalação ative a `virtualenv` criada executando o arquivo 

```shell script
$ source ./<pasta_onde_o_poetry_criou_a_virtualenv>/bin/activate
````

## Variáveis de ambiente

Antes de rodar a plicação é necessário configurar as variáveis de ambiente.
Renomeie o arquivo `local.env` para `.env` e preencha cada uma das variáveis com os valores conforme descrito abaixo:

`SECRET_KEY` =  Crie uma chave utilizando o comando:
```shell script
$ make generate_secret_key
```
Copie a chave gerada e atribua a variável.


`API_URL` = Cole a URL da API externa para exibir o acumulado de cashback

`API_TOKEN` = Cole o token de acesso a API externa

## Rodando os testes unitários

Rode os testes unitários com o comando:

```shell script
$ make test
```

## Rodando o projeto

O próximo passo é rodar o projeto e para isso utilize o comando:

```shell script
$ make runserver
```

\o/\o/\o/ Show de bola! Agora vamos conhecer os endpoints da API.

## Endpoints da API

Host: `http://127.0.0.1:8000/api`

### Endpoint: `/seller/register/`

Neste recurso é possível cadastrar revendedores.

Tipos de requests: [`POST`]

Payload:
```json
{
    "username": "teste",
    "first_name": "teste",
    "last_name": "teste",
    "email": "teste@boticario.com",
    "document": "12345678901",
    "password": "123456"
}
```
Response:
```json
{
    "username": "teste",
    "first_name": "teste",
    "last_name": "teste",
    "email": "teste@boticario.com",
    "document": "12345678901",
    "password": "***********"
}
```

### Endpoint: `/token/`

Este endpoint permite obter o token de acesso.

Tipos de requests: [`POST`]

Payload:
```json
{
    "username": "username",
    "password": "123456"
}
```
Response:
```json
{
  "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU",
  "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"
}

```

## Endpoints privados

A partir de agora, todas as requisições deverão conter no `Header` o token de acesso, exemplo:

```json

{"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU"}

```

### Cadastrar vendas `/cashback/`

Este endpoint permite que o revendedor logado cadastre de novas vendas.

Tipos de requests: [`GET`, `POST`]

#### Request POST
Payload:
```json
{
    "code" : "1231234",
    "amount": "2000",
    "date": "2020-11-11"
}
```
Response:
```json
{
    "code": "1231234",
    "amount": "2000.00",
    "date": "2020-11-11",
    "status": "Aprovado",
    "cashback_percent": "20",
    "cashback_value": "400.00",
    "created_at": "2020-11-19"
}
```

#### Request GET

Response:

```json
[
    {
        "code": "123123",
        "amount": "2000.00",
        "date": "2020-11-11",
        "status": "Aprovado",
        "cashback_percent": "20",
        "cashback_value": "400.00",
        "created_at": "2020-11-19"
    },
    {
        "code": "3434",
        "amount": "2000.00",
        "date": "2020-11-11",
        "status": "Aprovado",
        "cashback_percent": "20",
        "cashback_value": "400.00",
        "created_at": "2020-11-19"
    }
]
```

### Endpoint `/cashback/amount/`

Este endpoint permite visualizar o acumulado de cashback.

Tipos de request: [`GET`]

Response:
```json
{
    "statusCode": 200,
    "body": {
        "credit": 4321
    }
}
```

## That's All!!! =)
