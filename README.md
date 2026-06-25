# donutstats

Async Python wrapper for the [DonutSMP](https://donutsmp.net) API.

![PyPI](https://img.shields.io/pypi/v/donutstats?cacheSeconds=3600) ![Python](https://img.shields.io/pypi/pyversions/donutstats?cacheSeconds=3600) ![License](https://img.shields.io/pypi/l/donutstats?cacheSeconds=3600)

[![tests](https://github.com/optccopa/donutstats/actions/workflows/tests.yml/badge.svg)](https://github.com/optccopa/donutstats/actions/workflows/tests.yml)

## Install

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
from donutstats import DonutStats

async def main():
    donutstats = DonutStats("Your DonutSMP api key (generate ingame with /api")

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

    await donutstats.close() # Close it when you close your bot

asyncio.run(main())
```
## Exceptions

- `DonutSMPError` - Raised when DonutSMP cannot handle a query, Very likely could not find username
- `UnauthorizedRequest` - Raised when DonutSMP returns a 401 unauthorized.
- `RateLimited` - Raised when DonutSMP returns a 429 ratelimited
- `UnexpectedError` - Raised when there is an unexpected api response status.

## License

MIT License [LICENSE](LICENSE)
