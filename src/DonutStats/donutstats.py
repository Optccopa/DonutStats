import aiohttp, json

class DonutSMPError(Exception):
    """Raised when donutsmp cannot handle a query, Very likely could not find username"""
    pass

class UnauthorizedRequest(Exception):
    """Raised when donutsmp returns a 401 unauthorized"""
    pass

class UnexpectedError(Exception):
    """Raised when there is an unexpected api response status"""
    pass

class DonutStats():
    def __init__(self, donutsmp_api_key: str):
        self._base_url = "https://api.donutsmp.net/v1"
        self._donutsmp_headers = {"Authorization": f"Bearer {donutsmp_api_key}"}
        self._session: aiohttp.ClientSession | None = None
        self._timeout = aiohttp.ClientTimeout(total=10)

    def _get_session(self) -> aiohttp.ClientSession:
        """Fetches the aiohttp session or creates a new one"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(timeout=self._timeout)
        return self._session

    async def get_stats(self, username: str) -> dict:
        """
        Returns a users donutsmp stats as a dict

        Response: 
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
        url = f"{self._base_url}/stats/{username}"
        session = self._get_session()
        async with session.get(url, headers=self._donutsmp_headers) as resp:
            if resp.status == 401:
                await self.close()
                raise UnauthorizedRequest("Please generate an API Key in game with /api and supply it when initializing this class")
            if resp.status != 200:
                await self.close()
                raise DonutSMPError(f"Unexpected status (Status: {resp.status})")

            text = await resp.text()
            data: dict = json.loads(text)
            return data.get('result')

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()

    async def close(self):
        """Close the aiohttp session"""
        if self._session and not self._session.closed:
            await self._session.close()
