# donutstats

Async Python client for the [DonutSMP](https://donutsmp.net) API.
## Install

```bash
pip install donutstats
```
## Usage

### Simple api usage
```python
import asyncio
from donutstats import DonutStats

async def main():
    donutstats = DonutStats("Your DonutSMP api key (generate ingame with /api)")

    # Full stats dict
    stats = await donutstats.get_stats(username="copa6076") # Pull the stats from donutsmp api
    print(stats.get('money')) # 2920840615

    # Single stat
    shards = await donutstats.get_shards(username="copa6076") # Pull the shards from donutsmp api
    print(shards) # 8410

    await donutstats.close() # Close it when you close your bot

asyncio.run(main())
```

# Simple discord bot cog usage
```python
import discord
from discord.ext import commands

class Stats(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.donutstats = donutstats.DonutStats("Your DonutSMP api key (generate ingame with /api")

    @discord.app_commands.command()
    async def stats(self, interaction: discord.Interaction, username: str):

        # Returns a full stats embed with a headm 
        embed: discord.Embed = await self.donutstats.get_stats_embed(username, discord.Color.blue())

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Stats(bot))
```
## Exceptions

- `DonutSMPError` — query could not be handled (likely unknown username).
- `UnauthorizedRequest` — 401, bad/missing API key.
- `UnexpectedError` — unexpected API response status.

## License

MIT License [LICENSE](LICENSE)
