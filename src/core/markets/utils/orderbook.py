from core.markets.models import Order


def raw_list_to_orders_tuple(raw: list[list[float]]) -> tuple[Order, ...]:
    return tuple(Order(float(p), float(q)) for p, q, *_ in raw)
