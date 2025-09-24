from time import time


def get_current_timestamp() -> int:
    return int(time() * 1000)


def get_normalized_symbol(symbol: str) -> str:
    return symbol.strip().upper()
