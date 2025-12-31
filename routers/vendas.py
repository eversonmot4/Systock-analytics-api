from fastapi import APIRouter, HTTPException
from typing import List
from services.repository import fetch_view
from schemas.generic import Row

router = APIRouter()


@router.get("/evolucao", response_model=List[Row])
def get_evolucao_vendas():
    try:
        rows = fetch_view("vw_evolucao_vendas")
        return [Row(__root__=r) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/semanais", response_model=List[Row])
def get_vendas_semanais():
    try:
        rows = fetch_view("vw_vendas_semanais")
        return [Row(__root__=r) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
