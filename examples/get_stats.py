import asyncio

from donutstats import DonutStats


async def main():
    donutstats = DonutStats("Your DonutSMP api key (generate ingame with /api)")

    # Pull the stats from donutsmp api via ign
    stats = await donutstats.get_stats(username="copa6076")

    print(stats.get("money"))  # 2920840615

    # Cleanly close the aiohttp connection; aiohttp gets loud about unclosed connections
    await donutstats.close()


asyncio.run(main())  # Start the async event loop
