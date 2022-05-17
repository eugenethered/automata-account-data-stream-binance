from binance.message.trade.transform.BinanceTradeMessageTransformer import BinanceTradeMessageTransformer
from tests.helper.ConfigReporterHolderHelper import ConfigReporterHolderHelper


class BinanceTradeMessageTransformerHelper(BinanceTradeMessageTransformer):

    def __init__(self, transformations):
        self.transformations = transformations
        self.config_reporter = ConfigReporterHolderHelper()
