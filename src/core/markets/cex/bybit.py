from core.markets.base.connections import AiohttpConnection
from core.markets.base.marketdata import MarketData
from core.models import OrderBook, Price, Symbol

BYBIT_API = 'https://api.bybit.com/v5'
PRICE_URL = f'{BYBIT_API}/market/tickers'
ORDERBOOK_URL = f'{BYBIT_API}/market/orderbook'


class ByBitData(AiohttpConnection, MarketData):
    async def fetch_price(self, symbol: Symbol) -> Price:
        params = {'category': 'spot', 'symbol': symbol.__str__()}
        raw = await self._fetch_json(PRICE_URL, params=params)
        return Price(
            symbol=symbol,
            value=float(raw['result']['list'][0]['lastPrice']),
            timestamp=int(raw['time']),
        )

    async def fetch_orders(self, symbol: Symbol, depth: int = 5) -> OrderBook:
        params = {
            'category': 'spot',
            'symbol': symbol.__str__(),
            'limit': str(depth),
        }
        raw = await self._fetch_json(ORDERBOOK_URL, params=params)
        return OrderBook(
            symbol=symbol,
            bids=[(float(p), float(q)) for p, q in raw['result']['b']],
            asks=[(float(p), float(q)) for p, q in raw['result']['a']],
            timestamp=int(raw['time']),
        )
