from abc import ABC, abstractmethod

from core.models import OrderBook, Price, Symbol


class MarketData(ABC):
    @abstractmethod
    async def fetch_price(self, symbol: Symbol) -> Price: ...

    @abstractmethod
    async def fetch_orders(
        self, symbol: Symbol, depth: int = 5
    ) -> OrderBook: ...
