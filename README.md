# SyStock Analytics API

Lightweight FastAPI application exposing read-only views from a data warehouse.

Overview
--------
API leve cuja responsabilidade é disponibilizar, via HTTP, resultados de views analíticas já existentes no Data Warehouse. A API apenas consulta essas views e entrega os registros em JSON, prontos para consumo por frontends ou ferramentas de BI.

Observação importante: esta API não executa ETL nem gerencia a infra do banco de dados.

Problem Statement
-----------------
Organizações precisam disponibilizar dados analíticos consolidados para dashboards e ferramentas de visualização sem expor mecanismos de escrita ou lógica de transformação no serviço de API. É necessário uma camada de leitura segura e simples que exponha as views já consolidadas no Data Warehouse.

Key Features
------------
- **API somente-leitura (read-only).**
- **Endpoints organizados por domínio**: vendas, lojas, produtos, estoque, categorias.
- **Segurança por whitelist de views (nomes de views controlados no código).**
- **Documentação automática via Swagger (OpenAPI).**
- **Respostas serializadas com Pydantic para consistência de contrato.**

Architecture & Components
------------
- FastAPI: roteamento e documentação automática.
- Routers: organização por domínio (ex.: `vendas.py`, `lojas.py`, etc.).
- Camada de acesso a dados (repository): responsável por executar `SELECT * FROM <view>` apenas para views autorizadas (whitelist).
- Conexão com banco obtida a partir de `DATABASE_URL`
- Dependência de um Data Warehouse PostgreSQL externo que contém as views consultadas.
- 
lllllllllllllllllllllllllllllllllllllllllllllllllll

Technologies
------------
- Python (3.10+)
- FastAPI
- SQLAlchemy (engine/core)
- Pydantic
- PostgreSQL (Data Warehouse)

Repository Layout (high level)
-----------------------------
- `main.py/` — aplicação FastAPI
- `database.py/` — carregamento de DATABASE_URL e criação do engine
- `routers/` — endpoints organizados por domínio
- `services/` — repository para leitura das views
- `schemas/` — modelos Pydantic
- `tests/` — scripts de verificação (ex.: `route_checks.py/`)
- `routers/` — endpoints organizados por domínio


Getting Started
---------------
Prerequisites: Docker and Docker Compose installed, and Python 3.9+ for local development.

Quick start (development with Docker):

```bash
# Start services and the local development environment
docker-compose up --build -d

# Run ETL pipeline (example entrypoint — adjust as needed)
docker-compose exec <service> python -m pipeline_manager.pipeline_flow
```

See [DOCKER_SETUP.md](DOCKER_SETUP.md) for full container configuration and [START_HERE.md](START_HERE.md) for project onboarding steps.

How to run locally
-------------------
You can run this project either using Docker Compose (recommended) or locally with Python for development. Choose the option that fits your environment.

- Requirements: Docker & Docker Compose (for Docker), Python 3.9+ and `pip` (for local development).

- Option A — Docker Compose (recommended):

```bash
# Start all services (Postgres, ETL, etc.)
docker-compose up --build -d

# Follow ETL container logs
docker-compose logs -f etl-pipeline

# Execute the main pipeline inside the ETL container
docker-compose exec etl-pipeline python -m pipeline_manager.pipeline_flow
```

Note: the ETL service is named `etl-pipeline` in [docker-compose.yml](docker-compose.yml).

- Option B — Run locally with Python (development):

1. Start only the database service (recommended) or ensure a PostgreSQL instance is available:

```bash
docker-compose up -d postgres-dw
```

2. Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Unix / macOS
source .venv/bin/activate

pip install -r etl_pipeline/requirements.txt
```

3. Configure required environment variables (`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`). Use a `.env` file or your shell to set them.

4. Run the pipeline locally:

```bash
python -m pipeline_manager.pipeline_flow
```

- Running tests:

```bash
pip install -r etl_pipeline/requirements.txt
pytest -q
```

Helpful files: [docker-compose.yml](docker-compose.yml), [etl_pipeline/requirements.txt](etl_pipeline/requirements.txt), and the pipeline entrypoint [pipeline_manager/pipeline_flow.py](pipeline_manager/pipeline_flow.py).

Development
-----------
To run tests locally (from a configured Python environment):

```bash
python -m pip install -r etl_pipeline/requirements.txt
pytest -q
```

For iterative development, run pipeline modules directly or use the provided orchestration in `pipeline_manager`.

Contributing
------------
Contributions are welcome. Please follow these guidelines:
- Open an issue to discuss major changes.
- Create feature branches and submit pull requests with descriptive titles.
- Include tests for new functionality where applicable.

License
-------
This project is licensed under the terms in the repository `LICENSE` file.
