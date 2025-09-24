from core.markets.cex.binance import BinanceData


async def main() -> None:
    symbol = 'BTCUSDDDT'

    async with BinanceData() as market:
        price = await market.fetch_price(symbol)
        orderbook = await market.fetch_orders(symbol)

    print(price)
    print(orderbook)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
