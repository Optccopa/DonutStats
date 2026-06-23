# donutstats

Async Python client for the [DonutSMP](https://donutsmp.net) API.
## Install

```bash
pip install donutstats
```
## Usage

```python
import asyncio
from DonutStats import DonutStats

async def main():
    donutstats = DonutStats("Your DonutSMP api key (generate ingame with /api)")

    stats = await donutstats.get_stats(username="copa6076") # Pull the stats from donutsmp api

    print(stats.get('money')) # 2920840615

    await donutstats.close()

asyncio.run(main())
```

## Exceptions

- `DonutSMPError` — query could not be handled (likely unknown username).
- `UnauthorizedRequest` — 401, bad/missing API key.
- `UnexpectedError` — unexpected API response status.

## License

MIT License [LICENSE](LICENSE)
