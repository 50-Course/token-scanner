from typing import Optional
from fastapi import APIRouter
from src.schemas import TokenResponse

router = APIRouter()


@router.get("/tokens/pools", response_model=list[TokenResponse])
async def fetch_token_info(
    token_address: str,
    chain_id: str,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
):
    pass
