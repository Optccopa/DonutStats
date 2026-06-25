from __future__ import annotations

import random
import string
from json import JSONDecodeError
from unittest.mock import AsyncMock, MagicMock

import aiohttp
import pytest


def rand_ign() -> str:
    """Random Minecraft-style username (3-16 chars). Mocked, so any name works."""
    length = random.randint(3, 16)
    return "".join(random.choices(string.ascii_letters + string.digits + "_", k=length))

from donutstats import (
    DonutStats,
    DonutSMPError,
    UnauthorizedRequest,
    RateLimited,
    UnexpectedError,
)
from donutstats.utils import fmt_amount, fmt_playtime

SAMPLE_RESULT = {
    "money": 2577174314,
    "shards": 8461,
    "kills": 24,
    "deaths": 92,
    "playtime": 1050579440,
    "placed_blocks": 7524,
    "broken_blocks": 7285,
    "mobs_killed": 63,
    "money_spent_on_shop": 2688539,
    "money_made_from_sell": 1.1477798052923137e+8,
}

# get_stats() coerces every field to int; this is what it returns for SAMPLE_RESULT.
EXPECTED_STATS = {key: int(value) for key, value in SAMPLE_RESULT.items()}

UNKNOWN_USER_BODY = {
    "status": 500,
    "reason": "Error handling request",
    "message": (
        "Could not handle your request. This may be because the "
        "specified user/page/item does not exist."
    ),
}

# Captured verbatim from a real GET /v1/lookup/copa6076 response body's `result`.
LOOKUP_RESULT = {
    "username": "copa6076",
    "rank": "Unknown",
    "location": "Overworld",
}

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


def make_client(
    *, status: int = 200, payload=None, json_exc: Exception | None = None,
    enter_exc: Exception | None = None,
) -> tuple[DonutStats, MagicMock]:
    resp = MagicMock()
    resp.status = status
    resp.text = AsyncMock(return_value="<mock body>")
    if json_exc is not None:
        resp.json = AsyncMock(side_effect=json_exc)
    else:
        resp.json = AsyncMock(return_value=payload)

    cm = MagicMock()
    if enter_exc is not None:
        cm.__aenter__ = AsyncMock(side_effect=enter_exc)
    else:
        cm.__aenter__ = AsyncMock(return_value=resp)
    cm.__aexit__ = AsyncMock(return_value=False)

    session = MagicMock()
    session.closed = False
    session.get = MagicMock(return_value=cm)
    session.close = AsyncMock()

    ds = DonutStats("fake-token")
    ds._session = session
    ds._resolve_session = lambda: session
    return ds, session

async def test_get_stats_returns_result_dict():
    ds, session = make_client(payload={"result": SAMPLE_RESULT})
    stats = await ds.get_stats("copa6076")
    assert stats == EXPECTED_STATS
    # auth header sent
    _, kwargs = session.get.call_args
    assert kwargs["headers"] == {"Authorization": "Bearer fake-token"}


async def test_get_stats_url_encodes_username():
    ds, session = make_client(payload={"result": SAMPLE_RESULT})
    await ds.get_stats("weird / name")
    url = session.get.call_args.args[0]
    assert url.endswith("/stats/weird%20%2F%20name")

@pytest.mark.parametrize(
    "status,exc",
    [
        (401, UnauthorizedRequest),
        (429, RateLimited),
        (404, DonutSMPError),
        (500, DonutSMPError),
    ],
)
async def test_status_codes_raise(status, exc):
    ds, _ = make_client(status=status, payload={"result": SAMPLE_RESULT})
    with pytest.raises(exc):
        await ds.get_stats("copa6076")


async def test_unknown_user_raises_donutsmp_error():
    ds, _ = make_client(status=500, payload=UNKNOWN_USER_BODY)
    with pytest.raises(DonutSMPError):
        await ds.get_stats(rand_ign())


async def test_invalid_json_raises_unexpected():
    ds, _ = make_client(json_exc=JSONDecodeError("bad", "doc", 0))
    with pytest.raises(UnexpectedError):
        await ds.get_stats("copa6076")


async def test_missing_result_field_raises_unexpected():
    ds, _ = make_client(payload={"something_else": 1})
    with pytest.raises(UnexpectedError):
        await ds.get_stats("copa6076")


async def test_client_error_wrapped_as_unexpected():
    ds, _ = make_client(enter_exc=aiohttp.ClientError("boom"))
    with pytest.raises(UnexpectedError):
        await ds.get_stats("copa6076")
@pytest.mark.parametrize("method", INT_METHODS)
async def test_int_methods_return_int(method):
    ds, _ = make_client(payload={"result": SAMPLE_RESULT})
    value = await getattr(ds, method)("copa6076")
    assert isinstance(value, int)
    assert value >= 0


async def test_balance_maps_to_money():
    ds, _ = make_client(payload={"result": SAMPLE_RESULT})
    assert await ds.get_balance("copa6076") == 2577174314


async def test_scientific_notation_parses():
    ds, _ = make_client(payload={"result": SAMPLE_RESULT})
    assert await ds.get_money_made_from_sell("copa6076") == 114777980


async def test_non_numeric_field_raises_unexpected():
    result = dict(SAMPLE_RESULT, kills="not-a-number")
    ds, _ = make_client(payload={"result": result})
    with pytest.raises(UnexpectedError):
        await ds.get_kills("copa6076")


async def test_missing_field_raises_unexpected():
    result = {k: v for k, v in SAMPLE_RESULT.items() if k != "shards"}
    ds, _ = make_client(payload={"result": result})
    with pytest.raises(UnexpectedError):
        await ds.get_shards("copa6076")


# --------------------------------------------------------------------------- #
# session lifecycle
# --------------------------------------------------------------------------- #
async def test_context_manager_closes_session():
    ds, session = make_client(payload={"result": SAMPLE_RESULT})
    async with ds as c:
        await c.get_stats("copa6076")
    session.close.assert_awaited_once()


async def test_close_is_idempotent_when_no_session():
    ds = DonutStats("fake-token")
    # never opened a session; close() must not blow up
    await ds.close()


# --------------------------------------------------------------------------- #
# formatting helpers (pure)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "value,expected",
    [
        (0, "0"),
        (500, "500"),
        (1500, "1.5k"),
        (8410, "8.41k"),
        (1_000_000, "1m"),
        (2_920_840_615, "2.92b"),
        (1_500_000_000_000, "1.5t"),
    ],
)
def test_fmt_amount(value, expected):
    assert fmt_amount(value) == expected


@pytest.mark.parametrize(
    "ms,expected",
    [
        (0, "0m"),
        (90_000, "1m"),
        (3_600_000, "1h"),
        (90_060_000, "1d 1h 1m"),
    ],
)
def test_fmt_playtime(ms, expected):
    assert fmt_playtime(ms) == expected


# --------------------------------------------------------------------------- #
# lookup (mirrors get_stats: same status branches + result unwrap)
# --------------------------------------------------------------------------- #
async def test_lookup_returns_result_dict():
    ds, session = make_client(payload={"result": LOOKUP_RESULT})
    result = await ds.lookup("copa6076")
    assert result == LOOKUP_RESULT
    # hits the lookup endpoint with the auth header
    args, kwargs = session.get.call_args
    assert args[0].endswith("/lookup/copa6076")
    assert kwargs["headers"] == {"Authorization": "Bearer fake-token"}


async def test_lookup_url_encodes_username():
    ds, session = make_client(payload={"result": LOOKUP_RESULT})
    await ds.lookup("weird / name")
    url = session.get.call_args.args[0]
    assert url.endswith("/lookup/weird%20%2F%20name")


@pytest.mark.parametrize(
    "status,exc",
    [
        (401, UnauthorizedRequest),
        (429, RateLimited),
        (404, DonutSMPError),
        (500, DonutSMPError),
    ],
)
async def test_lookup_status_codes_raise(status, exc):
    ds, _ = make_client(status=status, payload={"result": LOOKUP_RESULT})
    with pytest.raises(exc):
        await ds.lookup("copa6076")


async def test_lookup_unknown_user_raises_donutsmp_error():
    ds, _ = make_client(status=500, payload=UNKNOWN_USER_BODY)
    with pytest.raises(DonutSMPError):
        await ds.lookup(rand_ign())


async def test_lookup_invalid_json_raises_unexpected():
    ds, _ = make_client(json_exc=JSONDecodeError("bad", "doc", 0))
    with pytest.raises(UnexpectedError):
        await ds.lookup("copa6076")


async def test_lookup_missing_result_field_raises_unexpected():
    ds, _ = make_client(payload={"something_else": 1})
    with pytest.raises(UnexpectedError):
        await ds.lookup("copa6076")


async def test_lookup_client_error_wrapped_as_unexpected():
    ds, _ = make_client(enter_exc=aiohttp.ClientError("boom"))
    with pytest.raises(UnexpectedError):
        await ds.lookup("copa6076")
