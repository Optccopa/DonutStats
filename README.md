# donutstats

Async Python wrapper for the [DonutSMP](https://donutsmp.net) API.

![PyPI](https://img.shields.io/pypi/v/donutstats) ![Python](https://img.shields.io/pypi/pyversions/donutstats) ![License](https://img.shields.io/pypi/l/donutstats)

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

### Simple api usage
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

    await donutstats.close() # Close it when you close your bot

asyncio.run(main())
```

### Simple discord bot cog usage
```python
import discord
from discord.ext import commands

from donutstats import DonutStats

class Stats(commands.Cog):
    def __init__(self, bot: commands.Bot):
        # Initialize donutstats when your cog gets initialized
        self.donutstats = DonutStats("Your DonutSMP api key (generate ingame with /api")

    @discord.app_commands.command()
    async def stats(self, interaction: discord.Interaction, username: str):
        # Returns a full stats embed
        embed: discord.Embed = await self.donutstats.get_stats_embed(username, discord.Color.blue())

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Stats(bot))
```
## Exceptions

- `DonutSMPError` - Raised when DonutSMP cannot handle a query, Very likely could not find username
- `UnauthorizedRequest` - Raised when DonutSMP returns a 401 unauthorized.
- `RateLimited` - Raised when DonutSMP returns a 429 ratelimited
- `UnexpectedError` - Raised when there is an unexpected api response status.

## License

MIT License [LICENSE](LICENSE)
