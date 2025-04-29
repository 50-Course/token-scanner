# Houses the Integration tests for our Token Scanner API

import pytest
from decimal import Decimal

from src.api.services import get_token_data


@pytest.mark.asyncio
async def test_fetch_token_data(monkeypatch):
    """Test the fetch_token_data function."""

    mocked_dex_data = [
        {
            "chainId": "solana",
            "liquidity": {"usd": 1000},
            "pairAddress": "A",
            "quoteToken": {"address": "Q1"},
            "baseToken": {"symbol": "T1"},
        },
        {
            "chainId": "solana",
            "liquidity": {"usd": 5000},
            "pairAddress": "B",
            "quoteToken": {"address": "Q2"},
            "baseToken": {"symbol": "T2"},
        },
        {
            "chainId": "ethereum",
            "liquidity": {"usd": 7000},
            "pairAddress": "C",
            "quoteToken": {"address": "Q3"},
            "baseToken": {"symbol": "T3"},
        },
        {
            "chainId": "solana",
            "pairAddress": "PAIR1",
            "liquidity": {"usd": "5000"},
            "quoteToken": {"address": "QUOTE1"},
            "baseToken": {"symbol": "TOKEN1"},
        },
        {
            "chainId": "solana",
            "pairAddress": "PAIR2",
            "liquidity": {"usd": "10000"},
            "quoteToken": {"address": "QUOTE2"},
            "baseToken": {"symbol": "TOKEN1"},
        },
    ]

    # we would set the mock_get_pools function to be the one that is called
    # See: https://docs.pytest.org/en/stable/how-to/monkeypatch.html
    async def mock_get_pools(chain_id, token_address):
        """Mock function to simulate fetching pools from the API."""
        return mocked_dex_data

    monkeypatch.setattr("src.api.services.fetch_token_pools", mock_get_pools)

    token_data_response = await get_token_data(
        chain_id="solana", token_address="TOKEN1"
    )
    assert token_data_response is not None
    assert token_data_response.pool_count == 4
    assert token_data_response.total_liquidity_usd == Decimal(21000)
    assert token_data_response.largest_pool.pair_address == "PAIR2"
