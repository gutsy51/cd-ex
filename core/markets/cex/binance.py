from core.markets.marketdata import MarketData
from core.models.ticker import Ticker, TickerPrice, TickerDepth
from core.utils import get_current_timestamp

BINANCE_API = 'https://api.binance.com/api/v3'
PRICE_URL = f'{BINANCE_API}/ticker/price'
DEPTH_URL = f'{BINANCE_API}/depth'


class BinanceData(MarketData):
    async def fetch_ticker_data(self, ticker: Ticker, depth: int = 5) -> Ticker:
        price = await self.fetch_price(ticker)
        depth = await self.fetch_depth(ticker, depth=depth)
        return Ticker(symbol=ticker.symbol, price=price, depth=depth)

    async def fetch_price(self, ticker: Ticker) -> TickerPrice:
        params = {'symbol': ticker.symbol}
        data = await self._fetch_data(PRICE_URL, params)
        price = TickerPrice()
        price.update(float(data['price']), timestamp=get_current_timestamp())
        return price

    async def fetch_depth(
            self, ticker: Ticker, depth: int = 5
    ) -> TickerDepth:
        params = {'symbol': ticker.symbol, 'limit': depth}
        data = await self._fetch_data(DEPTH_URL, params)
        orderbook = TickerDepth()
        bids = [(float(p), float(q)) for p, q in data.get('bids', [])]
        asks = [(float(p), float(q)) for p, q in data.get('asks', [])]
        orderbook.update(bids, asks, timestamp=get_current_timestamp())
        return orderbook
