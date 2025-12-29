from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routers import vendas, lojas, categorias, produtos, estoque
from database import engine

app = FastAPI(title="SyStock Analytics API", version="0.1.0", description="Read-only analytics views for SyStock")

# incluir routers
app.include_router(vendas.router, prefix="/vendas", tags=["vendas"])
app.include_router(lojas.router, prefix="/lojas", tags=["lojas"])
app.include_router(categorias.router, prefix="/categorias", tags=["categorias"])
app.include_router(produtos.router, prefix="/produtos", tags=["produtos"])
app.include_router(estoque.router, prefix="/estoque", tags=["estoque"])


@app.on_event("startup")
def startup():
    # Verificação rápida da conexão com o engine do banco
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
    except Exception:
        # Mantém o serviço em execução; erros detalhados aparecerão nas chamadas dos endpoints
        pass


@app.get("/health")
def health():
    return JSONResponse({"status": "ok"})
