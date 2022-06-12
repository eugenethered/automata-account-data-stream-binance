from data.websocket.WebSocketRunner import WebSocketRunner
from positionrepo.repository.PositionRepository import PositionRepository
from processmanager.ProcessBase import ProcessBase
from traderepo.repository.TradeRepository import TradeRepository
from tradetransformrepo.repository.TradeTransformRepository import TradeTransformRepository

from binance.auth.BinanceAuthenticator import BinanceAuthenticator
from binance.message.trade.BinanceTradeDataMessageProcessor import BinanceTradeDataMessageProcessor
from binance.message.trade.handler.BinanceTradeDataMessageHandler import BinanceTradeDataMessageHandler
from binance.message.trade.transform.BinanceTradeMessageTransformer import BinanceTradeMessageTransformer
from binance.payload.BinanceDataPayloadProcessor import BinanceDataPayloadProcessor


class BinanceAccountDataStream(ProcessBase):

    def __init__(self, url, options):
        super().__init__(options, 'binance', 'account-data-stream')
        self.options = options
        self.url = url
        authenticator = BinanceAuthenticator(self.options)
        trade_message_processor = self.init_trade_message_processor()
        payload_processor = BinanceDataPayloadProcessor([trade_message_processor])
        self.ws_runner = WebSocketRunner(self.url, payload_processor, ping_interval=8, authenticator=authenticator)
        self.init_web_socket_callbacks()

    def init_web_socket_callbacks(self):
        self.ws_runner.set_stopped_callback(self.process_stopped)
        self.ws_runner.set_running_callback(self.process_running)
        self.ws_runner.set_error_callback(self.process_error)

    def init_trade_message_processor(self):
        trade_transform_repository = TradeTransformRepository(self.options)
        message_transformer = BinanceTradeMessageTransformer(trade_transform_repository)
        trade_repository = TradeRepository(self.options)
        position_repository = PositionRepository(self.options)
        message_handler = BinanceTradeDataMessageHandler(trade_repository, position_repository)
        return BinanceTradeDataMessageProcessor(message_transformer, message_handler)

    def receive_data(self):
        self.ws_runner.receive_data()
