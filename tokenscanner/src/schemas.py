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

    class Config:
        json_schema_extra = {
            "example": {
                "name": "solana",
                "pool_address": "3nX2fG7qTz9p1jWqL9vJHaRbVcXJe4PsKy5wE8MCYrAU",
                "pair_address": "PAIR1",
                "liquidity_usd": "5000.00",
                "quote_token_address": "6sTv9jKbYrMdZNEE82vPWeAcLdBzvFnkC3gLFKwXcFzT",
            }
        }


class TokenResponse(BaseModel):
    address: str  # Address of the token
    largest_pool: Optional[PoolInfo]
    total_liquidity_usd: Decimal
    pool_count: int  # number of pools the token is in

    class Config:
        json_schema_extra = {
            "example": {
                "address": "hex1234567890abcdef1234567890abcdef12345678",
                "largest_pool": {
                    "name": "USDC59780a5436ce4acd8534d430e3f9a3e9",
                    "pool_address": "hexnewpooladdress1234567890abcdef12345678",
                    "pair_address": "hexpairaddress1234567890abcdef12345678",
                    "liquidity_usd": "5000.00",
                    "quote_token_address": "7305ae2adaaa49f1b5474bca47fb17f8",
                },
                "total_liquidity_usd": "15000.00",
                "pool_count": 3,
            }
        }
