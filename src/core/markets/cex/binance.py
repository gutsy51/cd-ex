from core.markets.base.connections import AiohttpConnection
from core.markets.base.marketdata import MarketData
from core.markets.models import OrderBook, Price, Symbol
from core.markets.utils.orderbook import raw_list_to_orders_tuple

BINANCE_API = 'https://api.binance.com/api/v3'
PRICE_URL = f'{BINANCE_API}/ticker/price'
ORDERBOOK_URL = f'{BINANCE_API}/depth'


class BinanceData(AiohttpConnection, MarketData):
    async def fetch_price(self, symbol: Symbol) -> Price:
        params = {'symbol': symbol.__str__()}
        raw = await self._fetch_json(PRICE_URL, params=params)
        return Price(symbol=symbol, value=float(raw['price']))

    async def fetch_orders(self, symbol: Symbol, depth: int = 5) -> OrderBook:
        params = {'symbol': symbol.__str__(), 'limit': str(depth)}
        raw = await self._fetch_json(ORDERBOOK_URL, params=params)
        return OrderBook(
            symbol=symbol,
            bids=raw_list_to_orders_tuple(raw['bids']),
            asks=raw_list_to_orders_tuple(raw['asks']),
        )
