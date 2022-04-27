from scripts.logic.PriceLogic import PriceLogic
from scripts.trading.TradingApi import TradingApi
from scripts.repository.Repository import Repository


class TradingBot(PriceLogic, TradingApi):
    def __init__(
        self, low, hight, intervals, initial_capital, tokenAddress, ownerAddress
    ):
        try:
            repository = Db()

