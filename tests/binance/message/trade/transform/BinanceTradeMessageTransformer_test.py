import unittest

from core.number.BigFloat import BigFloat
from core.trade.Order import OrderType, Status

from binance.message.trade.transform.error.OrderTransformException import OrderTransformException
from tests.helper.BinanceTradeMessageTransformerHelper import BinanceTradeMessageTransformerHelper


class BinanceTradeMessageTransformerTestCase(unittest.TestCase):

    def setUp(self):
        transformations = {
            ('OTCBTC', 'SELL'): 'OTC/BTC'
        }
        self.message_transformer = BinanceTradeMessageTransformerHelper(transformations)

    def test_should_transform_order_parts_into_new_order(self):
        order = self.message_transformer.transform('OTCBTC', 'SELL', '100.01', '8888-8888', 'MARKET', 'NEW', 1, None, None)
        self.assertEqual(order.instrument_from, 'OTC')
        self.assertEqual(order.instrument_to, 'BTC')
        self.assertEqual(order.quantity, BigFloat('100.01'))
        self.assertEqual(order.order_id, '8888-8888')
        self.assertEqual(order.order_type, OrderType.MARKET)
        self.assertEqual(order.status, Status.NEW)
        self.assertEqual(order.instant, 1)
        self.assertEqual(order.price, None)
        self.assertEqual(order.value, None)

    def test_should_transform_order_parts_into_executed_order_with_value_and_price(self):
        order = self.message_transformer.transform('OTCBTC', 'SELL', '100.01', '8888-8888', 'MARKET', 'FILLED', 1, '1.01', '101.0101')
        self.assertEqual(order.instrument_from, 'OTC')
        self.assertEqual(order.instrument_to, 'BTC')
        self.assertEqual(order.quantity, BigFloat('100.01'))
        self.assertEqual(order.order_id, '8888-8888')
        self.assertEqual(order.order_type, OrderType.MARKET)
        self.assertEqual(order.status, Status.EXECUTED)
        self.assertEqual(order.instant, 1)
        self.assertEqual(order.price, BigFloat('1.01'))
        self.assertEqual(order.value, BigFloat('101.0101'))

    def test_should_not_transform_to_order_when_transformation_is_missing(self):
        with self.assertRaises(OrderTransformException):
            self.message_transformer.transform('OTCUKO', 'SELL', '100.01', '8888-8888', 'MARKET', 'NEW', 1, '1.01', '101.0101')
        config_reporter = self.message_transformer.config_reporter
        self.assertEqual(config_reporter.missing.missing, 'OTCUKO+SELL')


if __name__ == '__main__':
    unittest.main()
