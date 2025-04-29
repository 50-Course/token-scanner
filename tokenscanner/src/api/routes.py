import logging

from typing import Optional
from fastapi import APIRouter, BackgroundTasks, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.exceptions import DEXScreenerAPIException, TokenNotFoundError
from src.api.openapi import POOL_DATA_ENDPOINT_DESCRIPTION, POOL_DATA_SUMMARY
from src.api.services import get_token_data, save_record
from src.core.db import get_db
from src.schemas import TokenResponse

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Pools"],
)


# essenitaly, we should throw this in a `constants.py` file
# and import it here. Hardcoding it here for now
MAX_PAGE_COUNT = 25


@router.get(
    "/tokens/pools",
    summary=POOL_DATA_SUMMARY,
    description=POOL_DATA_ENDPOINT_DESCRIPTION,
    responses={
        404: {"description": "Token not found. Please check the address."},
        500: {"description": "Internal server error. Please try again later."},
    },
    response_model=list[TokenResponse],
)
async def fetch_token_info(
    background_tasks: BackgroundTasks,
    token_address: str = Query(
        ...,
        description="Token address to fetch data for. \
                          Can be a single address or a comma-separated list of addresses",
    ),
    chain_id: str = Query(
        ...,
        regex="^(sol|ethereum|bsc)$",
        description="Blockchain to fetch token data from. Supported \
                          chains: Ethereum (ETH), Solana (SOL), Binance Smart Chain(BSC)",
    ),
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    db: AsyncSession = Depends(get_db),
):
    result = []

    addresses = [addr.strip() for addr in token_address if addr.split(",")]
    for addr in addresses:
        try:
            token_info = await get_token_data(addr, chain_id)
            result.append(token_info)

            # here we paginate
            # TODO: come back to this, perhaps at later date
            if len(result) >= MAX_PAGE_COUNT:
                pass

            # save to hot cache (our db) in the background
            background_tasks.add_task(
                save_record, chain_id, addr, token_info.largest_pool.dict(), db
            )
        except TokenNotFoundError as err:
            logger.error(f"Token {addr} not found on chain {chain_id}. Error: {err}")
            continue
        except DEXScreenerAPIException:
            raise HTTPException(
                status_code=502,
                detail=f"Error fetching data for token {addr} on chain {chain_id}",
            )

    # result here is just list of Token Responses, we should now have our
    return result
