from typing import Any

from aiohttp import ClientError, ClientResponseError

from core.markets.base.connections import AiohttpConnection
from core.markets.base.marketdata import AsyncMarketData

BINANCE_API = 'https://api.binance.com/api/v3'
PRICE_URL = f'{BINANCE_API}/ticker/price'
DEPTH_URL = f'{BINANCE_API}/depth'


class BinanceData(AiohttpConnection, AsyncMarketData):
    async def _fetch_price_json(self, symbol: str) -> dict[str, str]:
        params = {'symbol': symbol}
        return await self.__fetch_json(PRICE_URL, params)

    async def _fetch_orders_json(
        self, symbol: str, depth: int
    ) -> dict[str, list[tuple[str, str]]]:
        params = {'symbol': symbol, 'limit': str(depth)}
        return await self.__fetch_json(DEPTH_URL, params)

    async def __fetch_json(
        self, url: str, params: dict[str, str]
    ) -> dict[str, Any]:
        try:
            async with self.session.get(url, params=params) as response:
                response.raise_for_status()
                data: dict[str, Any] = await response.json()
                return data
        except ClientResponseError as e:
            raise RuntimeError(f'HTTP{e.status} ({e.message})') from e
        except ClientError as e:
            raise RuntimeError(f'Client error: {e}') from e
