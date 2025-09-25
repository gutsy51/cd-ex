from core.markets.cex.binance import BinanceData
from core.markets.cex.bybit import ByBitData
from core.markets.cex.coinbase import CoinbaseData
from core.models import Symbol


async def main() -> None:
    symbol = Symbol('BTC', 'USDT')

    async with BinanceData() as market:
        binance_price = await market.fetch_price(symbol)
        binance_orderbook = await market.fetch_orders(symbol)

    async with ByBitData() as market:
        bybit_price = await market.fetch_price(symbol)
        bybit_orderbook = await market.fetch_orders(symbol)

    async with CoinbaseData() as market:
        coinbase_price = await market.fetch_price(symbol)
        coinbase_orderbook = await market.fetch_orders(symbol)

    print(f'[ Binance] {binance_price}')
    print(f'[   ByBit] {bybit_price}')
    print(f'[Coinbase] {coinbase_price}')
    print()
    print(f'[ Binance] {binance_orderbook}')
    print(f'[   ByBit] {bybit_orderbook}')
    print(f'[Coinbase] {coinbase_orderbook}')


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
