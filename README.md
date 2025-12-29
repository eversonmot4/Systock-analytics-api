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
- Camada de acesso a dados (repository): responsável por executar SELECT * FROM <view> apenas para views autorizadas (whitelist).
- Conexão com banco obtida a partir de `DATABASE_URL`
- Dependência de um Data Warehouse PostgreSQL externo que contém as views consultadas.
