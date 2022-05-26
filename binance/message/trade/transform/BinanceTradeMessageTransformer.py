import logging
from typing import List

from config.report.holder.ConfigReporterHolder import ConfigReporterHolder
from core.missing.Context import Context
from core.number.BigFloat import BigFloat
from core.trade.Order import Order, OrderType, Status
from coreutility.collection.dictionary_utility import as_data
from missingrepo.Missing import Missing
from tradetransformrepo.TradeTransform import TradeTransform
from tradetransformrepo.repository.TradeTransformRepository import TradeTransformRepository

from binance.message.trade.transform.error.OrderTransformException import OrderTransformException


class BinanceTradeMessageTransformer:

    def __init__(self, repository: TradeTransformRepository):
        self.log = logging.getLogger(__name__)
        self.repository = repository
        self.transformations = self.load_transformations()
        self.config_reporter = ConfigReporterHolder()

    def load_transformations(self):
        trade_transformations = self.repository.retrieve()
        return dict(self.unpack_transformations(trade_transformations))

    def unpack_transformations(self, trade_transformations: List[TradeTransform]):
        for trade_transform in trade_transformations:
            yield self.build_transformation_key(trade_transform.transform), trade_transform.trade

    @staticmethod
    def build_transformation_key(transform):
        instrument = as_data(transform, 'instrument')
        side = as_data(transform, 'side')
        return instrument, side

    def transform(self, symbol, side, quantity, order_id, order_type, status, event_time, price, value) -> Order:
        if (symbol, side) in self.transformations:
            self.log.debug(f'Transformation being applied to symbol:{symbol} and side:{side}')
            trade = self.transformations[(symbol, side)]
            (instrument_from, instrument_to) = trade.split('/')
            return self.transform_to_order(instrument_from, instrument_to, quantity, order_id, order_type, status, event_time, price, value)
        else:
            self.report_missing_order(symbol, side)
            raise OrderTransformException(f'{symbol} and {side} does not have a trade transformation')

    def transform_to_order(self, instrument_from, instrument_to, quantity, order_id, raw_order_type, status, event_time, price, value) -> Order:
        order_quantity = self.obtain_big_float_value(quantity)
        order_type = OrderType.parse(raw_order_type)
        order_status = self.obtain_order_status(status)
        order = Order(instrument_from, instrument_to, order_quantity, order_id, order_type, order_status, event_time)
        self.set_order_price(order, price)
        self.set_order_value(order, value)
        return order

    @staticmethod
    def obtain_order_status(status_value):
        status_normalized = status_value.upper()
        if status_normalized == 'NEW':
            return Status.NEW
        elif status_normalized == 'FILLED':
            return Status.EXECUTED
        # todo: handle other cases (error, other side-effects)

    def set_order_value(self, order, value):
        order_value = self.obtain_big_float_value(value)
        if order_value is not None:
            order.value = order_value

    def set_order_price(self, order, price):
        order_price = self.obtain_big_float_value(price)
        if order_price is not None:
            order.price = order_price

    @staticmethod
    def obtain_big_float_value(value):
        result = BigFloat(value)
        return None if result.is_zero() is True else result

    def report_missing_order(self, instrument, side):
        self.log.warning(f'No Trade Transformation for instrument:{instrument} and side:{side}')
        missing_instrument_side = f'{instrument}+{side}'
        missing = Missing(missing_instrument_side, Context.TRADE, 'binance', f'Catastrophic cannot transform order for instrument:[{instrument}] and side:[{side}]')
        self.config_reporter.report_missing(missing)
