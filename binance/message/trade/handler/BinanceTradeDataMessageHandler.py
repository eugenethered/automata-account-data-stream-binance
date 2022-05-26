from core.position.Position import Position
from core.trade.InstrumentTrade import Status as TradeStatus, InstrumentTrade
from core.trade.Order import Order
from core.trade.Order import Status as OrderStatus
from positionrepo.repository.PositionRepository import PositionRepository
from traderepo.repository.TradeRepository import TradeRepository


class BinanceTradeDataMessageHandler:

    def __init__(self, trade_repository: TradeRepository, position_repository: PositionRepository):
        self.trade_repository = trade_repository
        self.position_repository = position_repository

    def handle_trade(self, order: Order):
        trade = self.trade_repository.retrieve_trade()
        if trade.order_id == order.order_id and trade.status == TradeStatus.SUBMITTED and order.status == OrderStatus.EXECUTED:
            trade.status = TradeStatus.EXECUTED
            trade.price = order.price
            trade.value = order.value
            trade.instant = order.instant
            self.trade_repository.store_trade(trade)
            self.create_position_from_trade(trade)

    def create_position_from_trade(self, trade: InstrumentTrade):
        instrument = trade.instrument_to
        # todo: verify
        quantity = trade.value
        instant = trade.instant
        exchanged_from = trade.instrument_from
        position = Position(instrument, quantity, instant, exchanged_from)
        self.position_repository.store(position)
