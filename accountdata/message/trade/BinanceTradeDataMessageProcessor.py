from data.message.DataMessageProcessor import DataMessageProcessor
from utility.json_utility import as_data

from binance.message.trade.handler.BinanceTradeDataMessageHandler import BinanceTradeDataMessageHandler
from binance.message.trade.transform.BinanceTradeMessageTransformer import BinanceTradeMessageTransformer


class BinanceTradeDataMessageProcessor(DataMessageProcessor):

    def __init__(self, message_transformer: BinanceTradeMessageTransformer, message_handler: BinanceTradeDataMessageHandler):
        # todo: need to obtain the correct stream
        super().__init__('????')
        self.message_transformer = message_transformer
        self.message_handler = message_handler

    def process_message(self, message):
        symbol = as_data(message, 's')
        quantity = as_data(message, 'q')
        order_id = as_data(message, 'i')
        order_type = as_data(message, 'o')
        status = as_data(message, 'X')
        event_time = as_data(message, 'E')
        order = self.message_transformer.transform(symbol, quantity, order_id, order_type, status, event_time)
        self.message_handler.handle_trade(order)
