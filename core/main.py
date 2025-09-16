from core.models.ticker import Ticker
from core.markets.cex.binance import BinanceData


async def main():
    ticker = Ticker('BTCUSDT')

    async with BinanceData() as market:
        ticker = await market.fetch_ticker_data(ticker)

    print(ticker)
    print(ticker.price)
    print(ticker.depth)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())