from dataclasses import dataclass

from core.utils import get_current_timestamp


@dataclass(frozen=True)
class Symbol:
    base: str
    quote: str

    def __str__(self) -> str:
        return f'{self.base}{self.quote}'


class TimestampedSymbol:
    _symbol: Symbol
    _timestamp: int

    def __init__(self, symbol: Symbol, timestamp: int | None = None) -> None:
        self._symbol = symbol
        self._timestamp = timestamp or get_current_timestamp()

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @property
    def symbol(self) -> Symbol:
        return self._symbol


class Price(TimestampedSymbol):
    __value: float

    def __init__(
        self, symbol: Symbol, value: float, timestamp: int | None = None
    ) -> None:
        super().__init__(symbol, timestamp)
        self.__value = value

    @property
    def value(self) -> float:
        return self.__value

    def update(self, value: float, timestamp: int | None = None) -> None:
        self.__value = value
        self._timestamp = timestamp or get_current_timestamp()

    def __str__(self) -> str:
        return f'{self.symbol} [ts={self.timestamp}]: price={self.value}'


class OrderBook(TimestampedSymbol):
    __bids: list[tuple[float, float]]
    __asks: list[tuple[float, float]]

    def __init__(
        self,
        symbol: Symbol,
        bids: list[tuple[float, float]],
        asks: list[tuple[float, float]],
        timestamp: int | None = None,
    ) -> None:
        super().__init__(symbol, timestamp)
        self.__bids = bids
        self.__asks = asks

    @property
    def bids(self) -> list[tuple[float, float]]:
        return self.__bids.copy()

    @property
    def asks(self) -> list[tuple[float, float]]:
        return self.__asks.copy()

    def update(
        self,
        bids: list[tuple[float, float]],
        asks: list[tuple[float, float]],
        timestamp: int | None = None,
    ) -> None:
        self.__bids = bids
        self.__asks = asks
        self._timestamp = timestamp or get_current_timestamp()

    def __str__(self) -> str:
        def to_str(x: list[tuple[float, float]]) -> str:
            return ', '.join(f'({p:.2f}, {q:.4f})' for p, q in x)

        bids_str = to_str(self.bids[:3]) or 'No bids'
        asks_str = to_str(self.asks[:3]) or 'No asks'
        return (
            f'{self.symbol} [ts={self.timestamp}]: '
            f'bids={bids_str}, asks={asks_str}'
        )
