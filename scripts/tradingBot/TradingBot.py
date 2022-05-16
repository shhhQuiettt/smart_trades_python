from scripts.logic.PriceLogic import PriceLogic
from scripts.trading.TradingApi import TradingApi
from scripts.repository.Repository import Repository
from os import environ


class TradingBot():
    def __init__(
            self, lowest_price: int, highest_price: int, intervals: int,
            initial_capital: int,
            ownerAddress: str, price_oracle_address: str, token: str,
            base_token: str
    ):
        """
        Parameters
        ----------
        NOTE that every token amount numbers must be in WEI notation!
        lowest_price: int
            predicted lowest price of the token in wei notation
        highest_price: int
            predicted highest price of the token in wei notation
        intervals: int
            number of orders equaly distributed between lowest_price
            and higest_price
        initial_capital: int
            initial capital of base token

        """
        repository_kwargs = {
            "db_address": environ["DB_ADDRESS"],
            "db_user": environ["DB_USER"],
            "db_password": environ["DB_PASSWORD"],
            "db_name": environ["TEST_DB_NAME"],
            "db_port": int(environ["DB_PORT"])
        }
        repository = Repository(**repository_kwargs)

        trading_api_kwargs = {
            price_oracle_address: price_oracle_address,
            token: token,
            base_token: base_token
        }
        trading_api = TradingApi
