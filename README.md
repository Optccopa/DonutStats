# donutstats

Async Python wrapper for the [DonutSMP](https://donutsmp.net) API.

![PyPI](https://img.shields.io/pypi/v/donutstats?cacheSeconds=3600)
[![Python](https://img.shields.io/pypi/pyversions/donutstats)](https://pypi.org/project/donutstats/)
[![PyPI Downloads](https://img.shields.io/pypi/dw/donutstats?cacheSeconds=3600)](https://pypi.org/project/donutstats/)

[![Tests](https://github.com/optccopa/donutstats/actions/workflows/tests.yml/badge.svg)](https://github.com/optccopa/donutstats/actions/workflows/tests.yml)
[![Lint](https://github.com/optccopa/donutstats/actions/workflows/lint.yml/badge.svg)](https://github.com/optccopa/donutstats/actions/workflows/lint.yml)
[![Types](https://img.shields.io/pypi/types/donutstats)](https://pypi.org/project/donutstats/)

## Install

Requires python 3.12 or newer
### Basic Install
```bash
pip install donutstats
```

### Discord Feature Usage
```bash
pip install donutstats[discord]
```

## Usage

### Simple stats usage
```python
import asyncio
from donutstats import DonutStats, DonutSMPError

async def main():
    donutstats = DonutStats("Your DonutSMP api key (generate ingame with /api)")

    # Full stats dict
    stats = await donutstats.get_stats(username="copa6076") # Pull the stats from donutsmp api
    print(stats.get('money')) # 2920840615

    # Single stat
    shards = await donutstats.get_shards(username="copa6076") # Pull the shards from donutsmp api
    print(shards) # 8410

    # Lookup
    lookup = await donutstats.lookup("copa6076")
    print(lookup) # {'username': 'copa6076', 'rank': 'Unknown', 'location': 'Overworld'}
    print(lookup.get('location')) # 'Overworld'

    # Unfound Player
    try:
        shards = await donutstats.get_shards(username="idontexist123d7") # Pull the shards from donutsmp api
        print(shards) # Doesnt run
    except DonutSMPError:
        # This code runs when the player is not found
        print("Could not find player")

    await donutstats.close() # Close it when you close your bot

asyncio.run(main())
```
## Functions
| Name | Args | Returns |
|---|---|---|
| `await get_stats` | `username: str` | `dict[str, int]` |
| `await lookup` | `username: str` | `dict[str, str]` |
| `await get_broken_blocks` | `username: str` | `int` |
| `await get_deaths` | `username: str` | `int` |
| `await get_kills` | `username: str` | `int` |
| `await get_mobs_killed` | `username: str` | `int` |
| `await get_balance` | `username: str` | `int` |
| `await get_money_made_from_sell` | `username: str` | `int` |
| `await get_money_spent_on_shop` | `username: str` | `int` |
| `await get_placed_blocks` | `username: str` | `int` |
| `await get_playtime` | `username: str` | `int` |
| `await get_shards` | `username: str` | `int` |
| `await get_stats_embed` | `username: str, color: discord.Color \| Default` | `discord.Embed` - requires `donutstats[discord]` |
| `await close` | `None` | `None` - Closes the session |
## Exceptions
| Name | Info |
|---|---|
| `DonutSMPError` | Raised when DonutSMP cannot handle a query - Likely cannot find player/page/item
| `UnauthorizedRequest` | Raised when DonutSMP returns a 401 unauthorized.
| `RateLimited` | Raised when DonutSMP returns a 429 ratelimited
| `UnexpectedErro r` | Raised when there is an unexpected api response status.

## License
Released under the MIT License. See [LICENSE](LICENSE).
