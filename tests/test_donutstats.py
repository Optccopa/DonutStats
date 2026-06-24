import asyncio
import os

import pytest
import pytest_asyncio
from dotenv import load_dotenv

# Seconds to wait after each test so the live API doesn't rate-limit (429) us
REQUEST_DELAY = 1.0

from donutstats import DonutStats, DonutSMPError, UnexpectedError

load_dotenv()
TOKEN = os.getenv("DONUTSMP_API_TOKEN")

# Every test below sends real requests to DonutSMP, so you must configure a token in .env
pytestmark = pytest.mark.skipif(
    not TOKEN, reason="DONUTSMP_API_TOKEN not set in .env"
)

# A real DonutSMP player to assert against
KNOWN_USER = "copa6076"

# Every method that returns a single int stat
INT_METHODS = [
    "get_broken_blocks",
    "get_deaths",
    "get_kills",
    "get_mobs_killed",
    "get_balance",
    "get_money_made_from_sell",
    "get_money_spent_on_shop",
    "get_placed_blocks",
    "get_playtime",
    "get_shards",
]

# Every key get_stats should return
STAT_KEYS = [
    "broken_blocks",
    "deaths",
    "kills",
    "mobs_killed",
    "money",
    "money_made_from_sell",
    "money_spent_on_shop",
    "placed_blocks",
    "playtime",
    "shards",
]


@pytest_asyncio.fixture(autouse=True)
async def _throttle():
    # Space out tests so the api doesnt ratelimit
    yield
    await asyncio.sleep(REQUEST_DELAY)


@pytest_asyncio.fixture
async def client():
    ds = DonutStats(TOKEN)
    yield ds
    await ds.close()


async def test_get_stats_returns_all_keys(client):
    stats = await client.get_stats(KNOWN_USER)
    assert isinstance(stats, dict)
    for key in STAT_KEYS:
        assert key in stats, f"missing key: {key}"
        assert isinstance(stats[key], str)


@pytest.mark.parametrize("method", INT_METHODS)
async def test_int_methods_return_nonnegative_int(client, method):
    value = await getattr(client, method)(KNOWN_USER)
    assert isinstance(value, int)
    assert value >= 0


@pytest.mark.parametrize("username", ["this_user_does_not_exist_xyz", "____", "a"])
async def test_unknown_user_raises(client, username):
    with pytest.raises((DonutSMPError, UnexpectedError)):
        await client.get_stats(username)


async def test_context_manager_closes_session():
    async with DonutStats(TOKEN) as ds:
        stats = await ds.get_stats(KNOWN_USER)
        assert "money" in stats
        session = ds._session
    assert session.closed
