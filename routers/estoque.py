from fastapi import APIRouter, HTTPException
from typing import List
from services.repository import fetch_view
from schemas.generic import Row

router = APIRouter()


@router.get("/valor-atual", response_model=List[Row])
def get_valor_estoque_atual():
    try:
        rows = fetch_view("vw_valor_estoque_atual")
        return [Row(__root__=r) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
