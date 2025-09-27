from core.markets.base.connections import AiohttpConnection
from core.markets.base.marketdata import MarketData
from core.markets.models import OrderBook, Price, Symbol
from core.markets.utils.orderbook import raw_list_to_orders_tuple
from core.markets.utils.timestamp import parse_iso8601_to_timestamp

COINBASE_API = 'https://api.exchange.coinbase.com'
PRICE_URL = f'{COINBASE_API}/products/{{symbol}}/ticker'
ORDERBOOK_URL = f'{COINBASE_API}/products/{{symbol}}/book'


class CoinbaseData(AiohttpConnection, MarketData):
    async def fetch_price(self, symbol: Symbol) -> Price:
        url = PRICE_URL.format(symbol=self.__symbol_to_str(symbol))
        raw = await self._fetch_json(url)
        return Price(
            symbol=symbol,
            value=float(raw['price']),
            timestamp=parse_iso8601_to_timestamp(raw['time']),
        )

    async def fetch_orders(self, symbol: Symbol, depth: int = 5) -> OrderBook:
        params = {'level': '2'}
        url = ORDERBOOK_URL.format(symbol=self.__symbol_to_str(symbol))
        raw = await self._fetch_json(url, params=params)
        return OrderBook(
            symbol=symbol,
            bids=raw_list_to_orders_tuple(raw['bids'][:depth]),
            asks=raw_list_to_orders_tuple(raw['asks'][:depth]),
            timestamp=parse_iso8601_to_timestamp(raw['time']),
        )

    @staticmethod
    def __symbol_to_str(symbol: Symbol) -> str:
        return f'{symbol.base}-{symbol.quote}'
