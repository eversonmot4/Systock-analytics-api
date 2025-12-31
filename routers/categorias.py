from fastapi import APIRouter, HTTPException
from typing import List
from services.repository import fetch_view
from schemas.generic import Row

router = APIRouter()


@router.get("/top", response_model=List[Row])
def get_top_categorias():
    try:
        rows = fetch_view("vw_categorias_mais_vendidas")
        return [Row(__root__=r) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
