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

# SyStock Analytics API

Aplicação FastAPI leve que expõe views somente-leitura de um Data Warehouse.

Início rápido

1. Copie `.env.example` para `.env` e defina `DATABASE_URL` (veja a seção "Banco" abaixo).
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute localmente:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Endpoints da API (documentação automática via Swagger):

- GET /vendas/evolucao
- GET /lojas/performance
- GET /categorias/top
- GET /produtos/top
- GET /estoque/valor-atual
- GET /vendas/semanais

Observações
- Este serviço é somente-leitura: executa `SELECT * FROM <view>` e retorna JSON.
- A API depende de um Data Warehouse PostgreSQL externo; o container ou o `docker-compose` do banco NÃO faz parte deste repositório.
- Não execute operações de escrita no banco a partir deste serviço.

Banco (exemplo para testes locais)
- Valores de ambiente de exemplo para testes locais:

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/systock_dw
DB_VIEW_PREFIX=data_warehouse.schema.views.
```

- `DATABASE_URL` é a única variável de ambiente usada para a conexão com o banco. `DB_VIEW_PREFIX` é usada apenas para prefixar os identificadores das views ao compor as queries somente-leitura.

Deploy
- Pode ser containerizado (ex.: `Dockerfile`) ou implantado em Railway/Render. Garanta que o ambiente forneça um `DATABASE_URL` acessível e que as views existam no schema/prefixo esperado.

Verificação de rotas (manual)
- Existe um pequeno script de verificação em `tests/route_checks.py`. Ele realiza requisições internas contra a aplicação FastAPI enquanto mocka a camada de repositório, portanto não requer o Data Warehouse real.
- Objetivo: checagem manual rápida para confirmar que todas as rotas estão conectadas e retornam respostas (útil antes de testes de integração ou deploys).
- Para executar localmente (em um virtualenv):

```bash
python -m pip install -r requirements.txt
python -m pip install httpx
python tests/route_checks.py
```

Não remova o script; ele destina-se à verificação manual local e a checagens leves de CI. Não faz parte da superfície de execução da API.
