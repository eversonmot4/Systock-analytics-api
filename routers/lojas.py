from fastapi import APIRouter, HTTPException
from typing import List
from services.repository import fetch_view
from schemas.generic import Row

router = APIRouter()


@router.get("/performance", response_model=List[Row])
def get_performance_loja():
    try:
        rows = fetch_view("view_preformance_loja")
        return [Row(__root__=r) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))