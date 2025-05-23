import httpx
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.exceptions import DEXScreenerAPIException, TokenNotFoundError
from src.core.config import settings
from src.models import Pool, Token
from src.schemas import PoolInfo, TokenResponse
from decimal import Decimal

logger = logging.getLogger(__name__)


async def fetch_token_pools(chain_id: str, token_address: str) -> list[dict]:
    DEX_POOL_API_BASE = f"{settings.DEXSCREENER_BASE_URI}/token-pairs/v1"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{DEX_POOL_API_BASE}/{chain_id}/{token_address}"
            )
            response.raise_for_status()

        data = response.json()

        if not isinstance(data, list) or len(data) == 0:
            logger.error("Invalid or empty response structure: %s", data)
            raise TokenNotFoundError(
                f"No pools found for {token_address} on {chain_id}"
            )

        return data

    except httpx.HTTPError as e:
        logger.error("HTTP error occurred: %s", e)
        raise DEXScreenerAPIException("Network error fetching token data: %s", e) from e

    except Exception as e:
        logger.exception("Error fetching token pools: %s", e)
        raise e


def filter_relevant_pools(pools: list[dict], chain_id: str) -> list[dict]:
    """Applys filter by chain/liquidity"""
    return [
        pool
        for pool in pools
        if pool["chainId"].lower() == chain_id.lower()
        and pool.get("liquidity", {}).get("usd", 0) > 0
    ]


def calculate_network_liquidity(pools: list[dict]) -> tuple[Decimal, dict]:
    """
    Computes the total liquidity and the largest pool
    """
    total = Decimal(0)  # we initial here, at zero
    largest = None

    for pool in pools:
        liquidity = Decimal(pool["liquidity"]["usd"])
        # increment the total reserve value
        total += liquidity

        if not largest or liquidity > Decimal(largest["liquidity"]["usd"]):
            largest = pool
    return total, largest  # type: ignore


async def save_record(
    chain_id: str, token_address: str, pool_data: dict, db: AsyncSession
) -> None:
    token_record = Token(
        chain_id=chain_id,
        address=token_address,
        # quote_token_address=pool_data["quote_token_address"],
        symbol=pool_data["name"].split("-", 1)[0],
        pool_count=pool_data.get("pool_count", 1),
        largest_pool_id=None,
        total_supply=None,
        total_liquidity_usd=pool_data["liquidity_usd"]
        or pool_data.get("total_liquidity_usd"),
    )

    db.add(token_record)
    await db.flush()

    pool_record = Pool(
        token_id=token_record.id,
        name=pool_data["name"],
        pool_address=pool_data["pool_address"],
        pair_address=pool_data["pair_address"],
        liquidity_usd=pool_data["liquidity_usd"],
        quote_token_address=pool_data["quote_token_address"],
    )

    db.add(pool_record)

    # we update our references to largest_pool_id with our Pool record object
    token_record.largest_pool_id = pool_record.id
    await db.commit()


async def get_token_data(token_address: str, chain_id: str) -> TokenResponse:
    # first we want to get the tokens from upstream
    pools = await fetch_token_pools(chain_id, token_address)

    # then we compare the "chain" to see if we looking at the right blockchain network
    # and therefore, its liquidity
    relevant_pools = [
        pool
        for pool in pools
        if pool["chainId"].lower() == chain_id.lower()
        and Decimal(pool.get("liquidity", {}).get("usd", 0) or 0)
        > 0  # force coersion to decimal
    ]

    if not relevant_pools:
        logger.error(
            "No relevant pools found for token %s on chain %s", token_address, chain_id
        )
        raise TokenNotFoundError(
            f"No valid pools found for {token_address} on {chain_id}"
        )

    total_liquidity, largest_pool = calculate_network_liquidity(relevant_pools)

    if not largest_pool or largest_pool is None:
        logger.error(
            "No largest pool found for token %s on chain %s", token_address, chain_id
        )
        raise TokenNotFoundError(
            f"No valid pools found for {token_address} on {chain_id}"
        )

    # then we return the token data (immediately, serialized) back to the handler
    # hence, faster feedback for interaction
    base_symbol = largest_pool["baseToken"]["symbol"]
    quote_symbol = largest_pool["quoteToken"].get("symbol")

    return TokenResponse(
        address=token_address,
        largest_pool=PoolInfo(
            name=f"{base_symbol}-{quote_symbol}",
            pool_address=largest_pool["pairAddress"],
            pair_address=largest_pool["pairAddress"],
            liquidity_usd=Decimal(largest_pool["liquidity"]["usd"]),
            quote_token_address=largest_pool["quoteToken"]["address"],
        ),
        total_liquidity_usd=total_liquidity,
        pool_count=len(relevant_pools),
    )
