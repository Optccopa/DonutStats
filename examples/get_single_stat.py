import asyncio
from donutstats import DonutStats

async def main():
    donutstats = DonutStats("Your DonutSMP api key (generate ingame with /api)")

    shards = await donutstats.get_shards(username="copa6076") # Pull the shards from donutsmp api via ign

    print(shards) # 8410

    await donutstats.close() # Cleanly close the aiohttp connection, aiohttp gets loud about unclosed connections

asyncio.run(main()) # Start the async event loop