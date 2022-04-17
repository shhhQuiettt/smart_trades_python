from logic import PriceLogic
from trading import TradingApi


class TradingBot(PriceLogic, TradingApi):
    def __init__(
        self, low, hight, intervals, initial_capital, tokenAddress, ownerAddress
    ):
        pass
