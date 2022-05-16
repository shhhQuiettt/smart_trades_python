import numpy
from .helpers import floor_decimal


class PriceLogic:
    def __init__(self, lowest_price, highest_price, intervals,
                 base_token_initial_capital: int,
                 token_initial_capital: int):
        self.lowest_price = lowest_price
        self.highest_price = highest_price
        self.intervals = intervals
        self.base_token_capital = base_token_initial_capital
        self.token_capital = token_initial_capital
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
            self.ba = -0.79 * self.base_token_capital / (
                    self.highest_price - self.lowest_price)
            self.bb = 0.8 * self.base_token_capital + 0.79 * self.lowest_price * self.base_token_capital / (
                    self.highest_price - self.lowest_price
            )

        if mode == "sell" or mode is None:
            self.sa = 0.79 * self.token_capital / (
                    self.highest_price - self.lowest_price)
            self.sb = 0.8 * self.token_capital - 0.79 * self.highest_price * self.token_capital / (
                    self.highest_price - self.lowest_price
            )

        if mode is not None and mode not in ["buy", "sell"]:
            raise ValueError("Invalide mode: has to be 'buy' or 'sell'")

    def get_amount_to_exchange(self, x, mode=None):
        if mode == "buy":
            return self.ba * x + self.bb
        if mode == "sell":
            return self.sa * x + self.sb
        raise ValueError('Mode has to be either "sell" or "buy"')

    if __name__ == "__main__":
        pass
