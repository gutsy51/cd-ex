from datetime import datetime
from time import time


def get_current_timestamp() -> int:
    return int(time() * 1000)


def parse_iso8601_to_timestamp(time_str: str) -> int:
    # Strip nanoseconds as datetime supports only microseconds.
    if '.' in time_str:
        base, frac = time_str.split('.')
        frac = frac.rstrip('Z')[:6]
        time_str = f"{base}.{frac}Z"

    dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return int(dt.timestamp() * 1000)


def get_normalized_symbol(symbol: str) -> str:
    return symbol.strip().upper()
