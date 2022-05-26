import logging

from binance.message.trade.transform.BinanceTradeMessageTransformer import BinanceTradeMessageTransformer
from tests.helper.ConfigReporterHolderHelper import ConfigReporterHolderHelper


class BinanceTradeMessageTransformerHelper(BinanceTradeMessageTransformer):

    def __init__(self, transformations):
        self.log = logging.getLogger(__name__)
        self.transformations = transformations
        self.config_reporter = ConfigReporterHolderHelper()
