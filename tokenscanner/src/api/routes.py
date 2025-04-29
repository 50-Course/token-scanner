import logging

from typing import Optional
from fastapi import APIRouter, BackgroundTasks, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.exceptions import (
    DEXScreenerAPIException,
    TokenNotFoundError,
    is_valid_solana_address,
)
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
    addresses: list[str] | str = Query(
        ...,
        description="Token address(es), to fetch data for.",
    ),
    chain_id: str = Query(
        ...,
        regex="^(solana|ethereum|bsc)$",
        alias="chain_id",
        description="Blockchain to fetch token data from. Supported \
                          chains: Ethereum (ETH), Solana (SOL), Binance Smart Chain(BSC)",
    ),
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    db: AsyncSession = Depends(get_db),
):
    result = []

    if isinstance(addresses, str):
        # if it's a single address, we need to split it into a list
        # and remove any whitespace
        addresses = [addr.strip() for addr in addresses.split(",") if addr.strip()]
    else:
        # if it's a list, we need to remove any whitespace
        # and make sure it's a list of strings
        addresses = [addr.strip() for addr in addresses]

    for addr in addresses:
        if chain_id == "solana" and not is_valid_solana_address(addr):
            logger.error(f"Invalid Solana address: {addr}")
            raise HTTPException(
                status_code=400,
                detail="Solana addresses cannot start with '0x'",
            )
        try:
            token_info = await get_token_data(addr, chain_id)

            logger.debug(f"Token info for {addr} on {chain_id}: {token_info}")
            result.append(token_info)

            # here we paginate
            # TODO: come back to this, perhaps at later date
            if len(result) >= MAX_PAGE_COUNT:
                break

            # save to hot cache (our db) in the background
            background_tasks.add_task(
                save_record, chain_id, addr, token_info.largest_pool.model_dump(), db
            )
        except TokenNotFoundError as err:
            logger.error(f"Token {addr} not found on chain {chain_id}. Error: {err}")
            raise HTTPException(
                status_code=404,
                detail=f"No pools found for token {addr} on chain {chain_id}. Please check the address.",
            )
        except DEXScreenerAPIException:
            raise HTTPException(
                status_code=502,
                detail=f"Error fetching data for token {addr} on chain {chain_id}",
            )

    # result here is just list of Token Responses, we should now have our
    return result
