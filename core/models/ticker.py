from dataclasses import dataclass, field
from typing import List, Tuple

from core.utils import get_current_timestamp


@dataclass()
class TickerPrice:
    __value: float | None = field(default=None, init=False)
    __timestamp: int | None = field(default=None, init=False)

    @property
    def value(self) -> float:
        if self.__value is None:
            raise ValueError('Price value is not set')
        return self.__value

    @property
    def timestamp(self) -> int:
        if self.__timestamp is None:
            raise ValueError('Price timestamp is not set')
        return self.__timestamp

    def update(self, value: float, timestamp: int | None = None):
        self.__value = value
        self.__timestamp = timestamp or get_current_timestamp()

    def __str__(self):
        if self.__value is None:
            return 'Price: <not set>'
        return f'Price at {self.__timestamp}: {self.__value:.8f}'


@dataclass()
class TickerDepth:
    __bids: List[Tuple[float, float]] = field(default_factory=list, init=False)
    __asks: List[Tuple[float, float]] = field(default_factory=list, init=False)
    __timestamp: int | None = field(default=None, init=False)

    @property
    def bids(self) -> List[Tuple[float, float]]:
        return self.__bids.copy()

    @property
    def asks(self) -> List[Tuple[float, float]]:
        return self.__asks.copy()

    @property
    def timestamp(self) -> int:
        if self.__timestamp is None:
            raise ValueError('Depth timestamp is not set')
        return self.__timestamp

    @property
    def depth(self) -> int:
        return len(self.__bids)

    def update(
            self,
            bids: List[Tuple[float, float]],
            asks: List[Tuple[float, float]],
            timestamp: int | None = None
    ):
        self.__bids = bids
        self.__asks = asks
        self.__timestamp = timestamp or get_current_timestamp()

    def __str__(self):
        bids_str = ', '.join(f'({p:.2f}, {q:.4f})' for p, q in self.__bids[:5])
        asks_str = ', '.join(f'({p:.2f}, {q:.4f})' for p, q in self.__asks[:5])
        return (f'Depth at {self.__timestamp}:\n  '
                f'Bids: [{bids_str}]\n  Asks: [{asks_str}]')


@dataclass
class Ticker:
    symbol: str
    price: TickerPrice = field(default_factory=TickerPrice)
    depth: TickerDepth = field(default_factory=TickerDepth)

    def __post_init__(self):
        self.symbol = self.symbol.strip().upper()

    def __str__(self):
        return f'{self.symbol}'

    def update_price(self, value: float, timestamp: int | None = None):
        self.price.update(value, timestamp)

    def update_depth(
            self,
            bids: List[Tuple[float, float]],
            asks: List[Tuple[float, float]],
            timestamp: int | None = None
    ):
        self.depth.update(bids, asks, timestamp)
