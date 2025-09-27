from dataclasses import dataclass

from core.markets.utils.timestamp import get_current_timestamp


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
        return f'{self.symbol} [ts={self.timestamp}]: price={self.__value}'


@dataclass(frozen=True)
class Order:
    price: float
    quantity: float

    def __str__(self) -> str:
        return f'({self.price}, {self.quantity})'


class OrderBook(TimestampedSymbol):
    __bids: tuple[Order, ...]
    __asks: tuple[Order, ...]

    def __init__(
        self,
        symbol: Symbol,
        bids: tuple[Order, ...],
        asks: tuple[Order, ...],
        timestamp: int | None = None,
    ) -> None:
        super().__init__(symbol, timestamp)
        self.__bids = bids
        self.__asks = asks

    @property
    def bids(self) -> tuple[Order, ...]:
        return self.__bids

    @property
    def asks(self) -> tuple[Order, ...]:
        return self.__asks

    def get_best_bid(self) -> Order | None:
        return self.__bids[0] if self.__bids else None

    def get_best_ask(self) -> Order | None:
        return self.__asks[0] if self.__asks else None

    def update(
        self,
        bids: tuple[Order, ...],
        asks: tuple[Order, ...],
        timestamp: int | None = None,
    ) -> None:
        self.__bids = bids
        self.__asks = asks
        self._timestamp = timestamp or get_current_timestamp()

    def __str__(self) -> str:
        def to_str(x: tuple[Order, ...]) -> str:
            return ', '.join(f'{order}' for order in x)

        bids_str = to_str(self.__bids[:3]) or 'No bids'
        asks_str = to_str(self.__asks[:3]) or 'No asks'
        return (
            f'{self.symbol} [ts={self.timestamp}]: '
            f'bids={bids_str}, asks={asks_str}'
        )
