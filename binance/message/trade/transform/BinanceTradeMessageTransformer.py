from typing import Optional

from core.trade.Order import Order


class BinanceTradeMessageTransformer:

    def __init__(self, options):
        pass

    def transform(self, symbol, quantity, order_id, order_type, status, event_time) -> Optional[Order]:
        pass
