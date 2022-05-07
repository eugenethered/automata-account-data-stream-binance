from data.websocket.WebSocketRunner import WebSocketRunner

from accountdata.message.trade.BinanceTradeDataMessageProcessor import BinanceTradeDataMessageProcessor
from accountdata.message.trade.handler.BinanceTradeDataMessageHandler import BinanceTradeDataMessageHandler
from accountdata.message.trade.transform.BinanceTradeMessageTransformer import BinanceTradeMessageTransformer
from accountdata.payload.BinanceDataPayloadProcessor import BinanceDataPayloadProcessor


class BinanceAccountDataStream:

    # todo: need to handle the "listen key" -> for orders
    def __init__(self, url, options):
        self.options = options
        self.url = url
        trade_message_processor = self.init_trade_message_processor()
        payload_processor = BinanceDataPayloadProcessor([trade_message_processor])
        self.ws_runner = WebSocketRunner(self.url, payload_processor)

    def init_trade_message_processor(self):
        message_transformer = BinanceTradeMessageTransformer(self.options)
        message_handler = BinanceTradeDataMessageHandler()
        return BinanceTradeDataMessageProcessor(message_transformer, message_handler)

    def receive_data(self):
        self.ws_runner.receive_data()
