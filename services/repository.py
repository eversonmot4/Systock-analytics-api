from typing import List, Dict, Any
from sqlalchemy import text
from database import engine, DB_VIEW_PREFIX


# Lista branca (whitelist) de nomes de views permitidas. Isso impede o uso
# de nomes fornecidos pelo usuário e mitiga o risco de SQL injection quando
# é necessário compor o identificador da tabela/view na string SQL.
ALLOWED_VIEWS = {
    "vw_evolucao_vendas",
    "vw_performance_lojas",
    "vw_categorias_mais_vendidas",
    "vw_produtos_mais_vendidos",
    "vw_valor_estoque_atual",
    "vw_vendas_semanais",
}


def _qualified(view_name: str) -> str:
    # Adiciona um prefixo opcional (schema) ao nome da view
    if DB_VIEW_PREFIX:
        return f"{DB_VIEW_PREFIX}{view_name}"
    return view_name


def fetch_view(view_name: str) -> List[Dict[str, Any]]:
    """Retorna linhas de uma view nomeada.

    A função aceita somente nomes presentes em `ALLOWED_VIEWS`.
    A SQL gerada é estritamente somente-leitura: `SELECT * FROM <view>`.

    Observação: o SQLAlchemy não permite parametrizar identificadores,
    portanto compor o identificador na string SQL é necessário — isso é
    seguro porque garantimos que o identificador venha da whitelist
    interna e não de entrada do usuário.
    """
    if view_name not in ALLOWED_VIEWS:
        raise ValueError("view não permitida")

    qualified = _qualified(view_name)
    qry = text(f"SELECT * FROM {qualified}")
    with engine.connect() as conn:
        result = conn.execute(qry)
        rows = [dict(row._mapping) for row in result]
    return rows