from abc import ABC, abstractmethod
from typing import Self

import aiohttp

from core.models.orderbook import OrderBook, Price


class MarketData(ABC):
    def __init__(self) -> None:
        self._session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> Self:
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(
        self, exc_type: type, exc_val: Exception, exc_tb: Exception
    ) -> None:
        if self._session:
            await self._session.close()
            self._session = None

    @property
    def session(self) -> aiohttp.ClientSession:
        if not self._session:
            raise RuntimeError('ClientSession is not initialized')
        return self._session

    @abstractmethod
    async def fetch_price(self, symbol: str) -> Price: ...

    @abstractmethod
    async def fetch_orders(self, symbol: str, depth: int = 5) -> OrderBook: ...
