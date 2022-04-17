import numpy
from .helpers import floor_decimal


class PriceLogic:
    def __init__(self, low, hight, intervals, initial_capital):
        self.low = low
        self.hight = hight
        self.intervals = intervals
        self.capital = initial_capital
        self.ba = 0
        self.bb = 0
        self.sa = 0
        self.sb = 0
        self.update_parameters()

    def update_parameters(self, mode=None):
        """
        get_parameters update parameters for get_usd_to_exchange function.
        param mode can  be either "sell" or "buy", update both if not defined.
        """
        if mode == "buy" or mode is None:
            self.ba = -0.79 * self.capital / (self.hight - self.low)
            self.bb = 0.8 * self.capital + 0.79 * self.low * self.capital / (
                self.hight - self.low
            )

        if mode == "sell" or mode is None:
            self.sa = 0.79 * self.capital / (self.hight - self.low)
            self.sb = 0.8 * self.capital - 0.79 * self.hight * self.capital / (
                self.hight - self.low
            )

        if mode is not None and mode not in ["buy", "sell"]:
            raise ValueError("Invalide mode: has to be 'buy' or 'sell'")

    def get_usd_to_exchange(self, x, mode=None):
        if mode == "buy":
            return self.ba * x + self.bb
        if mode == "sell":
            return self.sa * x + self.sb
        raise ValueError('Mode has to be either "sell" or "buy"')

    if __name__ == "__main__":
        pass
