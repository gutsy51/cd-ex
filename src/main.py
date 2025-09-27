from core.markets.cex.binance import BinanceData
from core.markets.cex.bybit import ByBitData
from core.markets.cex.coinbase import CoinbaseData
from core.markets.models import OrderBook, Price, Symbol


async def try_fetch(
    market: BinanceData | ByBitData | CoinbaseData, symbol: Symbol
) -> tuple[Price | None, OrderBook | None]:
    try:
        async with market as _market:
            price = await _market.fetch_price(symbol)
            orderbook = await _market.fetch_orders(symbol, 100)
        return price, orderbook
    except RuntimeError as e:
        print(e)
        return None, None


async def main() -> None:
    symbol = Symbol('XRP', 'USDT')

    binance_price, binance_orderbook = await try_fetch(BinanceData(), symbol)
    bybit_price, bybit_orderbook = await try_fetch(ByBitData(), symbol)
    coinbase_price, coinbase_orderbook = await try_fetch(CoinbaseData(), symbol)

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
