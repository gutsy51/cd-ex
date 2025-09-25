from abc import ABC, abstractmethod

from core.models import OrderBook, Price


class AsyncMarketData(ABC):
    """Asynchronous market data getter interface.

    To use with specific market, you have to:
    - Implement _fetch_price_json and _fetch_orders_json
    - Implement or inherit Connection method
    """

    async def fetch_price(self, symbol: str) -> Price:
        raw = await self._fetch_price_json(symbol)
        return Price(symbol, float(raw['price']))

    async def fetch_orders(self, symbol: str, depth: int = 5) -> OrderBook:
        raw = await self._fetch_orders_json(symbol, depth)
        return OrderBook(
            symbol=symbol,
            bids=[(float(p), float(q)) for p, q in raw.get('bids', [])],
            asks=[(float(p), float(q)) for p, q in raw.get('asks', [])],
        )

    @abstractmethod
    async def _fetch_price_json(self, symbol: str) -> dict[str, str]: ...

    @abstractmethod
    async def _fetch_orders_json(
        self, symbol: str, depth: int
    ) -> dict[str, list[tuple[str, str]]]: ...
