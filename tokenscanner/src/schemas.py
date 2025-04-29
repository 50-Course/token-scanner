from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class TokenRequest(BaseModel):
    """Defines the request body for token scanning"""

    token: str
    address: str | list[str]


class PoolInfo(BaseModel):
    """Defines the information about a single pool"""

    name: Optional[str]
    pool_address: str
    pair_address: str
    liquidity_usd: Decimal
    quote_token_address: str  # Address of the token in the pool


class TokenResponse(BaseModel):
    address: str  # Address of the token
    largest_pool: Optional[PoolInfo]
    total_liquidity_usd: Decimal
    pool_count: int  # number of pools the token is in
