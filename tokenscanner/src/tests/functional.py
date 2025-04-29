import pytest
from decimal import Decimal
from src.api.services import calculate_network_liquidity, filter_relevant_pools


@pytest.fixture
def mock_pools():
    # quick pool response example to mock our dexscanner api
    return [
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
    ]


def test_filter_relevant_pools(mock_pools):
    filtered = filter_relevant_pools(mock_pools, "solana")

    assert len(filtered) == 2
    # ensure name match works as it shouldk
    assert all(p["chainId"] == "solana" for p in filtered)


def test_calculate_network_liquidity(mock_pools):
    # perform checks that verifys the compute logic
    # for calculating the total liquidity and finding the largest pool
    filtered = filter_relevant_pools(mock_pools, "solana")
    total_liquidity, largest_pool = calculate_network_liquidity(filtered)

    assert total_liquidity == Decimal(6000)
    assert largest_pool["pairAddress"] == "B"
