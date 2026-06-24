from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

import aiohttp
from json import JSONDecodeError
from urllib.parse import quote
from typing_extensions import deprecated
from .utils import fmt_amount, fmt_playtime

try:
    import discord
    _DISCORD = True
except ImportError:
    _DISCORD = False
    logger.warning("Some functionality requires discord.py, Install with: pip install donutstats[discord]")

class DonutSMPError(Exception):
    """Raised when DonutSMP cannot handle a query, Very likely could not find username"""
    pass

class UnauthorizedRequest(Exception):
    """Raised when DonutSMP returns a 401 unauthorized"""
    pass

class RateLimited(Exception):
    """Raised when DonutSMP returns a 429 ratelimited"""

class UnexpectedError(Exception):
    """Raised when there is an unexpected api response status"""
    pass

class DonutStats:
    def __init__(self, donutsmp_api_key: str):
        self._base_url = "https://api.donutsmp.net/v1"
        self._donutsmp_headers = {"Authorization": f"Bearer {donutsmp_api_key}"}
        self._session: aiohttp.ClientSession | None = None
        self._timeout = aiohttp.ClientTimeout(total=10)

    def _resolve_session(self) -> aiohttp.ClientSession:
        """Fetches the aiohttp session or creates a new one"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(timeout=self._timeout)
        return self._session

    async def get_stats(self, username: str) -> dict[str, str]:
        """
        Returns a users donutsmp stats as a dict

        Stats: 
            broken_blocks         string
            deaths	              string
            kills                 string
            mobs_killed           string
            money                 string
            money_made_from_sell  string
            money_spent_on_shop	  string
            placed_blocks         string
            playtime              string
            shards                string
        """
        url = f"{self._base_url}/stats/{quote(username, safe='')}"
        session = self._resolve_session()
        try:
            async with session.get(url, headers=self._donutsmp_headers) as resp:
                if resp.status == 401:
                    raise UnauthorizedRequest("Please generate an API Key in game with /api and supply it when initializing this class")
                if resp.status == 429:
                    raise RateLimited(f"Ratelimited, DonutSMP currently has a ratelimit of 250 Reqs / Second")
                if resp.status != 200:
                    raise DonutSMPError(f"Could not handle your request. This may be because the specified user/page/item does not exist. (Status: {resp.status})")
                try:
                    data: dict = await resp.json(content_type=None)
                except JSONDecodeError as e:
                    raise UnexpectedError("DonutSMP API failed to return valid json") from e
                result = data.get('result')
                if result is None:
                    raise UnexpectedError(f"The DonutSMP api failed to return a result field")
                return result
        except aiohttp.ClientError as e:
            raise UnexpectedError("Aiohttp had a ClientError, Refer to the traceback") from e
        
    async def _get_stat(self, username: str, field: str) -> int:
        """Fetch a single stat field for a user and convert it to an int"""
        stats = await self.get_stats(username=username)
        strfield = stats.get(field)
        try:
            return int(strfield)
        except (ValueError, TypeError) as e:
            raise UnexpectedError(f"DonutSMP failed to return a valid '{field}' field (Got: {strfield})") from e

    async def get_broken_blocks(self, username: str) -> int:
        """Returns a users DonutSMP broken blocks"""
        return await self._get_stat(username, "broken_blocks")

    async def get_deaths(self, username: str) -> int:
        """Returns a users DonutSMP deaths"""
        return await self._get_stat(username, "deaths")

    async def get_kills(self, username: str) -> int:
        """Returns a users DonutSMP kills"""
        return await self._get_stat(username, "kills")

    async def get_mobs_killed(self, username: str) -> int:
        """Returns a users DonutSMP mobs killed"""
        return await self._get_stat(username, "mobs_killed")

    async def get_balance(self, username: str) -> int:
        """Returns a users DonutSMP balance"""
        return await self._get_stat(username, "money")
    
    async def get_money_made_from_sell(self, username: str) -> int:
        """Returns a users DonutSMP money made from sell"""
        return await self._get_stat(username, "money_made_from_sell")
    
    @deprecated("DonutSMP removed /shop and replaced it with quickbuy, The API still returns old data.")
    async def get_money_spent_on_shop(self, username: str) -> int:
        """Returns a users DonutSMP money spent on shop"""
        return await self._get_stat(username, "money_spent_on_shop")

    async def get_placed_blocks(self, username: str) -> int:
        """Returns a users DonutSMP placed blocks"""
        return await self._get_stat(username, "placed_blocks")

    async def get_playtime(self, username: str) -> int:
        """Returns a users DonutSMP playtime"""
        return await self._get_stat(username, "playtime")

    async def get_shards(self, username: str) -> int:
        """Returns a users DonutSMP shards"""
        return await self._get_stat(username, "shards")
    
    async def get_stats_embed(self, username: str, color: discord.Color | None = None):
        """Returns a premade stats embed, REQUIRES pip install donutstats[discord]"""
        if not _DISCORD:
            raise RuntimeError("get_stats_embed() requires donutstats[discord], Install with: pip install donutstats[discord]")
        stats: dict = await self.get_stats(username=username)
        if color is None:
            color = discord.Color.blurple()
        embed = discord.Embed(
            title=f"{username}'s Stats",
            description=(
                f"**Balance:** {fmt_amount(stats['money'])}\n"
                f"**Shards:** {fmt_amount(stats['shards'])}\n"
                f"**Playtime:** {fmt_playtime(int(stats['playtime']))}\n"
                f"**Kills:** {fmt_amount(stats['kills'])}\n"
                f"**Deaths:** {fmt_amount(stats['deaths'])}\n"
                f"**Blocks Placed:** {fmt_amount(stats['placed_blocks'])}\n"
                f"**Blocks Broken:** {fmt_amount(stats['broken_blocks'])}\n"
                f"**Mobs Killed:** {fmt_amount(stats['mobs_killed'])}\n"
                f"**Money Spent On /shop:** {fmt_amount(stats['money_spent_on_shop'])}\n"
                f"**Money Made From /sell:** {fmt_amount(stats['money_made_from_sell'])}"
            ),
            color=color
        )
        embed.set_thumbnail(url=f"https://mc-heads.net/avatar/{username}")

        return embed

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()

    async def close(self):
        """Close the aiohttp session"""
        if self._session and not self._session.closed:
            await self._session.close()
