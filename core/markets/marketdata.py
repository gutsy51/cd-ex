import aiohttp
from abc import ABC, abstractmethod
from core.models.ticker import Ticker, TickerPrice, TickerDepth


class MarketData(ABC):
    def __init__(self):
        self._session: aiohttp.ClientSession | None = None

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()
            self._session = None

    @property
    def session(self) -> aiohttp.ClientSession:
        if not self._session:
            raise RuntimeError('ClientSession is not initialized')
        return self._session

    async def _fetch_data(self, url: str, params: dict) -> dict:
        async with self.session.get(url, params=params) as resp:
            return await resp.json()

    @abstractmethod
    async def fetch_ticker_data(self, ticker: Ticker, depth: int = 5) -> Ticker:
        """Fetch Ticker with filled price and depth."""
        ...

    @abstractmethod
    async def fetch_price(self, ticker: Ticker) -> TickerPrice: ...

    @abstractmethod
    async def fetch_depth(self, ticker: Ticker, depth: int = 5) -> TickerDepth: ...
