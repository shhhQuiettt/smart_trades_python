from scripts.helpful_scripts import get_account
from brownie import interface, config, network
from time import time
from datetime import timedelta


class TradingApi:

    def __init__(self, price_oracle_address, token, seconds_to_deadline, base_token="dai", debug=False):
        """
        token_address has to be specified when we want to swap
        dai for ERC20 token eg. WETH
        """
        self.account = get_account()
        self.network = network.show_active()

        self.token = token
        self.token_address = config["networks"][self.network]["token"][token]
        self.token_contract = interface.IERC20(self.token_address)

        self.base_token = base_token
        self.base_token_address = config["networks"][self.network]["token"][base_token]
        self.base_token_contract = interface.IERC20(self.base_token_address)

        self.price_oracle_address = price_oracle_address
        self.seconds_to_deadline = seconds_to_deadline

        # obtain necessary contract
        self.price_oracle = interface.AggregatorV3Interface(self.price_oracle_address)

        self.uniswap_v2_router_address = config["networks"][self.network]["uniswap_v2_router_02"]
        self.uniswap_v2_router = interface.IUniswapV2Router02(self.uniswap_v2_router_address)

        self.transaction_kwargs = {"from": self.account} if not debug else {"from": self.account,
                                                                            "gas_limit": 12_000_000,
                                                                            "allow_revert": True}

    def getBalance(self):
        balance = {
            "ETH": self.account.balance(),
            self.token: interface.IERC20(self.token_address).balanceOf(self.account.address),
            self.base_token: interface.IERC20(self.base_token_address).balanceOf(self.account.address),
        }
        return balance

    def getTokenPrice(self):
        _, price, _, _, _ = self.price_oracle.latestRoundData()
        return price

    def buy(self, baseTokensToExchange):
        pass
        # # amountOutMin = self.getTokenPrice() * usdToExchange
        # # converting to wei notation
        # baseTokensToExchange *= 10 ** 18
        #
        # # approving spent token
        # approve_tx = self.base_token_contract.approve(self.uniswap_v2_router_address, baseTokensToExchange,
        #                                               {"from": self.account})
        # approve_tx.wait(1)
        #
        # amountOutMin = 10 ** -9
        # path = [self.base_token_address, self.uniswap_v2_router.WETH()]  # self.token_address]
        # deadline = time() + self.seconds_to_deadline
        #
        # tx = self.uniswap_v2_router.swapExactTokensForTokens(baseTokensToExchange, amountOutMin, path,
        #                                                      self.account.address,
        #                                                      deadline, {"from": self.account, "allow_revert": True})
        # # return spent, received
        # return tx

    def sell(self, tokensToExchange):
        """
        param TokensToExchange: has to be in wei notation
        """

        # approving spent token
        approve_tx = self.token_contract.approve(self.uniswap_v2_router_address, tokensToExchange,
                                                 {"from": self.account})
        approve_tx.wait(1)

        amount_out_min = 0.985 * 10 ** 18 * tokensToExchange / self.getTokenPrice()
        print(f"{amount_out_min=}")
        path = [self.token_address, self.base_token_address]
        deadline = time() + self.seconds_to_deadline

        tx = self.uniswap_v2_router.swapExactTokensForTokens(tokensToExchange, amount_out_min, path,
                                                             self.account.address,
                                                             deadline, self.transaction_kwargs)
        tx.wait(1)

        # return spent, received
        return tx
