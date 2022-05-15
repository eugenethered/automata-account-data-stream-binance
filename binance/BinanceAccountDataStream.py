from data.websocket.WebSocketRunner import WebSocketRunner

from binance.auth.BinanceAuthenticator import BinanceAuthenticator
from binance.message.trade.BinanceTradeDataMessageProcessor import BinanceTradeDataMessageProcessor
from binance.message.trade.handler.BinanceTradeDataMessageHandler import BinanceTradeDataMessageHandler
from binance.message.trade.transform.BinanceTradeMessageTransformer import BinanceTradeMessageTransformer
from binance.payload.BinanceDataPayloadProcessor import BinanceDataPayloadProcessor


class BinanceAccountDataStream:

    def __init__(self, url, options):
        self.options = options
        self.url = url
        authenticator = BinanceAuthenticator(self.options)
        trade_message_processor = self.init_trade_message_processor()
        payload_processor = BinanceDataPayloadProcessor([trade_message_processor])
        self.ws_runner = WebSocketRunner(self.url, payload_processor, ping_interval=8, authenticator=authenticator)

    def init_trade_message_processor(self):
        message_transformer = BinanceTradeMessageTransformer(self.options)
        message_handler = BinanceTradeDataMessageHandler()
        return BinanceTradeDataMessageProcessor(message_transformer, message_handler)

    def receive_data(self):
        self.ws_runner.receive_data()
