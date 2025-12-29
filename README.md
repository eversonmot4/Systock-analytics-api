# SyStock Analytics API

**Nome do projeto**  
SyStock Analytics API

**Short description**  
API REST somente-leitura em FastAPI que expõe views analíticas de um Data Warehouse PostgreSQL para consumo por dashboards.

## Overview

API leve cujo propósito é disponibilizar via HTTP os resultados de views analíticas já existentes no Data Warehouse. A aplicação consulta essas views e retorna registros em JSON, prontos para consumo por frontends ou ferramentas de BI.

Importante: esta API não executa ETL nem gerencia a infraestrutura do banco de dados.

## Problem Statement

Organizações precisam expor dados analíticos consolidados para dashboards e ferramentas de visualização sem abrir mecanismos de escrita ou adicionar lógica de transformação na camada de API. É necessária uma camada de leitura segura, simples e auditável que entregue os conjuntos de dados consolidados já criados no Data Warehouse.

## Key Features

- API somente-leitura (read-only).
- Endpoints organizados por domínio: vendas, lojas, produtos, estoque, categorias.
- Segurança por whitelist de views (nomes de views controlados no código).
- Documentação automática via Swagger (OpenAPI).
- Respostas serializadas via Pydantic para consistência do contrato.

## Architecture & Components

- FastAPI: roteamento, validação e documentação automática.
- Routers: organização por domínio (ex.: `routers/vendas.py`, `routers/lojas.py`).
- Camada de acesso a dados (repository): executa `SELECT * FROM <view>` apenas para views autorizadas (whitelist).
- Conexão com o banco obtida a partir de `DATABASE_URL`.
- Dependência de um Data Warehouse PostgreSQL externo que contém as views consultadas.

## Technologies

- Python 3.10+
- FastAPI
- SQLAlchemy (engine/core)
- Pydantic
- PostgreSQL (Data Warehouse)

## Repository Layout (high level)

- `main.py` — aplicação FastAPI (entrada)
- `database.py` — carregamento de `DATABASE_URL` e criação do engine
- `routers/` — endpoints por domínio (`vendas.py`, `lojas.py`, `categorias.py`, `produtos.py`, `estoque.py`)
- `services/` — repository para leitura das views
- `schemas/` — modelos Pydantic
- `tests/` — scripts de verificação (ex.: `tests/route_checks.py`)
- `.env.example`, `requirements.txt`, `Dockerfile`, `.gitignore`, `README.md`

## Getting Started

Pré-requisitos
- Python 3.10+ instalado
- Acesso de rede ao Data Warehouse quando necessário para integração

Passos iniciais
1. Clonar o repositório:
```bash
git clone <url-do-repositorio>
cd <repositorio>
```
2. Criar e ativar um ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate
```

## How to run locally

1. Criar um arquivo `.env` a partir de `.env.example` e preencher as variáveis mínimas:

Exemplo de `.env` para testes locais:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/systock_dw
DB_VIEW_PREFIX=data_warehouse.schema.views.
```

- `DATABASE_URL` (obrigatório): string de conexão com o PostgreSQL que será usada para criar o engine.
- `DB_VIEW_PREFIX` (opcional): prefixo aplicado ao identificador da view quando necessário (ex.: `data_warehouse.schema.views.`). A composição final é `<DB_VIEW_PREFIX><view_name>`.

2. Instalar dependências:
```bash
python -m pip install -r requirements.txt
```

3. Subir a API localmente:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Aviso explícito: o Data Warehouse é externo a este repositório; **não** existe `docker-compose` do banco neste projeto. Garanta que `DATABASE_URL` aponte para uma instância com as views já criadas.

## Verificação manual das rotas

Existe um script de verificação manual em `tests/route_checks.py` com as seguintes características:
- Realiza requisições internas à aplicação via `TestClient`.
- Mocka a camada de repositório para não depender do banco real.
- Verifica que os endpoints configurados respondem corretamente (HTTP 200) e que as rotas estão devidamente expostas.

Como executar:
```bash
python -m pip install -r requirements.txt
python -m pip install httpx
python tests/route_checks.py
```

Nota: o script usa mocks e **não** requer conexão com o Data Warehouse.

## Development / Testing

- Utilize um ambiente virtual isolado (`.venv`).
- `tests/route_checks.py` fornece uma verificação rápida de roteamento; não há testes de integração com o banco neste repositório.
- Para alterações que exigem validação com o DW real, execute testes de integração em um ambiente controlado que disponha das views necessárias.

## Contributing

- Abra issues para discutir mudanças ou reportar problemas.
- Envie pull requests pequenos e focados; inclua descrição clara das mudanças.
- Não introduza operações de escrita no banco nem modifique a whitelist de views sem justificativa técnica e revisão.
- Atualize `requirements.txt` se adicionar dependências.

## License

Verifique o arquivo `LICENSE` no repositório para os termos de licença aplicáveis.
# SyStock Analytics API

Lightweight FastAPI application exposing read-only views from a data warehouse.

Quick start

1. Copy `.env.example` to `.env` and set `DATABASE_URL` (see Database section below).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run locally:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API endpoints (auto-documented via Swagger):

- GET /vendas/evolucao
- GET /lojas/performance
- GET /categorias/top
- GET /produtos/top
- GET /estoque/valor-atual
- GET /vendas/semanais

## Notas
- Este serviço é somente leitura: executa `SELECT * FROM <view>` e retorna JSON.
- A API depende de um Data Warehouse PostgreSQL externo; o container do banco ou arquivo de compose **NÃO** faz parte deste repositório.
- Não execute nenhuma operação de escrita no banco a partir deste serviço.

## Banco de Dados (exemplo de teste local)
- Valores de ambiente de exemplo para testes locais:

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/systock_dw
DB_VIEW_PREFIX=data_warehouse.schema.views.
```


- `DATABASE_URL` é a única variável de ambiente usada para a conexão com o banco.  
- `DB_VIEW_PREFIX` é usada apenas para prefixar os identificadores das views ao compor as consultas somente leitura.

## Deploy
- Pode ser containerizado (Dockerfile fornecido) ou implantado no Railway/Render.
- Garanta que o ambiente de destino forneça um `DATABASE_URL` acessível e que as views existam no schema/prefixo esperado.
