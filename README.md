# SyStock Analytics API

API REST desenvolvida com **FastAPI** para disponibilizar dados analíticos de um **Data Warehouse PostgreSQL**. O serviço consulta views previamente criadas e retorna os resultados em JSON para consumo por dashboards, aplicações frontend e ferramentas de Business Intelligence (BI).

> **Importante:** esta API é somente leitura. Ela não executa processos de ETL, não realiza operações de escrita e não gerencia a infraestrutura do Data Warehouse.

## Objetivo

Oferecer uma camada HTTP simples e controlada para consultar dados consolidados no Data Warehouse, sem expor operações de alteração no banco nem adicionar regras de transformação à camada da API.

## Funcionalidades

- **Consultas somente leitura:** acesso aos dados por meio de instruções `SELECT`.
- **Endpoints por domínio:** rotas organizadas para vendas, lojas, categorias, produtos e estoque.
- **Whitelist de views:** somente views previamente autorizadas no código podem ser consultadas.
- **Documentação OpenAPI:** documentação interativa gerada pelo FastAPI.
- **Validação com Pydantic:** respostas estruturadas para manter a consistência do contrato da API.

## Tecnologias

| Tecnologia | Finalidade |
|---|---|
| Python 3.10+ | Linguagem de desenvolvimento |
| FastAPI | Construção da API REST |
| SQLAlchemy | Conexão e acesso ao banco de dados |
| Pydantic | Validação e serialização de dados |
| PostgreSQL | Banco de dados do Data Warehouse |

## Arquitetura

A aplicação está organizada em componentes com responsabilidades específicas:

- **FastAPI:** gerencia o roteamento, a validação e a documentação da API.
- **Routers:** agrupam os endpoints por domínio de negócio.
- **Repository (`services/`):** executa consultas nas views autorizadas pela whitelist.
- **Database (`database.py`):** carrega a variável `DATABASE_URL` e configura o engine do SQLAlchemy.
- **Schemas (`schemas/`):** definem os modelos Pydantic utilizados na estruturação das respostas.

O acesso aos dados depende de um Data Warehouse PostgreSQL externo, que deve conter as views consultadas pela aplicação.

## Estrutura do projeto

```text
.
├── main.py                 # Inicialização da aplicação FastAPI
├── database.py             # Configuração da conexão com o banco
├── routers/                # Endpoints organizados por domínio
│   ├── vendas.py
│   ├── lojas.py
│   ├── categorias.py
│   ├── produtos.py
│   └── estoque.py
├── services/               # Camada de acesso às views
├── schemas/                # Modelos Pydantic
├── tests/                  # Scripts de verificação
│   └── route_checks.py
├── .env.example            # Exemplo de configuração das variáveis
├── requirements.txt        # Dependências Python
├── Dockerfile              # Configuração para containerização
├── .gitignore
└── README.md
```

## Endpoints disponíveis

As rotas abaixo são disponibilizadas pelo serviço e documentadas automaticamente pelo Swagger/OpenAPI.

| Método | Endpoint |
|---|---|
| `GET` | `/vendas/evolucao` |
| `GET` | `/vendas/semanais` |
| `GET` | `/lojas/performance` |
| `GET` | `/categorias/top` |
| `GET` | `/produtos/top` |
| `GET` | `/estoque/valor-atual` |

## Como executar localmente

### Pré-requisitos

- Python 3.10 ou superior.
- Acesso ao Data Warehouse PostgreSQL que contém as views utilizadas pela API.
- Git instalado para clonar o repositório.

### 1. Clone o repositório

```bash
git clone https://github.com/eversonmot4/Systock-analytics-api.git
cd Systock-analytics-api
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv .venv
```

No Linux ou macOS:

```bash
source .venv/bin/activate
```

No Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Instale as dependências

```bash
python -m pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie o arquivo `.env` com base no modelo disponibilizado:

```bash
cp .env.example .env
```

Configure os valores necessários no arquivo `.env`:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/systock_dw
DB_VIEW_PREFIX=data_warehouse.schema.views.
```

| Variável | Obrigatória | Descrição |
|---|---|---|
| `DATABASE_URL` | Sim | String de conexão utilizada para criar o engine do SQLAlchemy. Deve apontar para uma instância PostgreSQL acessível. |
| `DB_VIEW_PREFIX` | Não | Prefixo aplicado ao nome da view na composição da consulta. O identificador final é formado por `<DB_VIEW_PREFIX><view_name>`. |

> Os valores acima são exemplos para configuração local. Substitua-os pelos dados de conexão e pelo prefixo correspondentes ao seu ambiente.

### 5. Inicie a aplicação

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Com a aplicação em execução, acesse:

- API local: `http://localhost:8000`
- Documentação Swagger: `http://localhost:8000/docs`

> **Atenção:** o Data Warehouse é externo a este repositório. Este projeto não inclui banco de dados nem arquivo `docker-compose` para iniciá-lo. Para que as consultas funcionem, `DATABASE_URL` deve apontar para uma instância que já possua as views necessárias.

## Verificação das rotas

O projeto inclui o script `tests/route_checks.py` para realizar uma verificação manual dos endpoints.

O script:

- utiliza o `TestClient` para realizar requisições internas à aplicação;
- substitui a camada de repositório por mocks, evitando consultas ao banco real;
- verifica se as rotas configuradas estão expostas e respondem com HTTP 200.

Para executar a verificação:

```bash
python -m pip install httpx
python tests/route_checks.py
```

A verificação utiliza mocks e, portanto, **não exige conexão com o Data Warehouse**. Ela valida o roteamento da aplicação, mas não substitui testes de integração com o banco de dados.

## Desenvolvimento e testes

- Utilize um ambiente virtual isolado (`.venv`).
- Execute `tests/route_checks.py` após alterações nas rotas.
- Quando uma mudança depender do comportamento das views ou da conexão com o PostgreSQL, valide-a também em um ambiente controlado com acesso ao Data Warehouse.
- Não adicione operações de escrita ao banco de dados.

## Deploy

O projeto inclui um `Dockerfile` e pode ser containerizado ou implantado em plataformas como Railway e Render. No ambiente de implantação, configure um `DATABASE_URL` acessível e garanta que as views esperadas estejam disponíveis no Data Warehouse.

## Contribuição

1. Abra uma *issue* para discutir mudanças ou relatar problemas.
2. Envie *pull requests* pequenos e focados, com uma descrição clara das alterações.
3. Atualize `requirements.txt` sempre que adicionar dependências.
4. Não altere a whitelist de views nem introduza operações de escrita sem justificativa técnica e revisão.

## Licença

Consulte o arquivo [`LICENSE`](LICENSE) do repositório para verificar os termos de uso e distribuição do projeto.
