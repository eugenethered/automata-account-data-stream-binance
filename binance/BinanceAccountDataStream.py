from data.websocket.WebSocketRunner import WebSocketRunner
from positionrepo.repository.PositionRepository import PositionRepository
from traderepo.repository.TradeRepository import TradeRepository
from tradetransformrepo.repository.TradeTransformRepository import TradeTransformRepository

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
        trade_transform_repository = TradeTransformRepository(self.options)
        message_transformer = BinanceTradeMessageTransformer(trade_transform_repository)
        trade_repository = TradeRepository(self.options)
        position_repository = PositionRepository(self.options)
        message_handler = BinanceTradeDataMessageHandler(trade_repository, position_repository)
        return BinanceTradeDataMessageProcessor(message_transformer, message_handler)

    def receive_data(self):
        self.ws_runner.receive_data()
