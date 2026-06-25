import asyncio

from donutstats import DonutStats


async def main():
    donutstats = DonutStats("Your DonutSMP api key (generate ingame with /api)")

    lookup = await donutstats.lookup("copa6076")

    print(lookup)  # {'username': 'copa6076', 'rank': 'Unknown', 'location': 'Overworld'}
    print(lookup.get("location"))  # 'Overworld'

    # Cleanly close the aiohttp connection; aiohttp gets loud about unclosed connections
    await donutstats.close()


asyncio.run(main())  # Start the async event loop
