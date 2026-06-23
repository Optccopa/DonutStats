import asyncio
from donutstats import DonutStats

async def main():
    donutstats = DonutStats("Your DonutSMP api key (generate ingame with /api)")

    stats = await donutstats.get_stats(username="copa6076") # Pull the stats from donutsmp api via ign

    print(stats.get('money')) # 2920840615

    await donutstats.close() # Close the aiohttp connection, aiohttp gets loud about unclosed connections

asyncio.run(main()) # Start the async event loop