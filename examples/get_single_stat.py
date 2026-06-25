import asyncio

from donutstats import DonutStats


async def main():
    donutstats = DonutStats("Your DonutSMP api key (generate ingame with /api)")

    # Pull the shards from donutsmp api via ign
    shards = await donutstats.get_shards(username="copa6076")

    print(shards)  # 8410

    # Cleanly close the aiohttp connection; aiohttp gets loud about unclosed connections
    await donutstats.close()


asyncio.run(main())  # Start the async event loop
