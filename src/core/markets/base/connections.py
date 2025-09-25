from typing import Any, Self

import aiohttp
from aiohttp import ClientError, ClientResponseError


class AiohttpConnection:
    """Asynchronous HTTP connection manager.

    Inherit this class and use _fetch_json method.
    """

    def __init__(self) -> None:
        self._session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> Self:
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(
        self, exc_type: type, exc_val: Exception, exc_tb: Exception
    ) -> None:
        if self._session:
            await self._session.close()
            self._session = None

    @property
    def session(self) -> aiohttp.ClientSession:
        if not self._session:
            raise RuntimeError('ClientSession is not initialized')
        return self._session

    async def _fetch_json(
        self, url: str, params: dict[str, str] | None = None
    ) -> dict[str, Any]:
        try:
            async with self.session.get(url, params=params) as response:
                response.raise_for_status()
                data: dict[str, Any] = await response.json()
                if not data:
                    raise RuntimeError('Empty response')
                return data
        except ClientResponseError as e:
            raise RuntimeError(
                f'HTTP{e.status} ({e.message}) at '
                f'{url} with params {params}'
            ) from e
        except ClientError as e:
            raise RuntimeError(f'Client error: {e}') from e
