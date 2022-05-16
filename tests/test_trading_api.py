from scripts.trading.TradingApi import TradingApi
from brownie import config, network
from scripts.tokens_provider import get_weth
from scripts.helpful_scripts import get_account


def test_get_price_returns_price_from_oracle_dai_eth():
    current_network = network.show_active()
    trading_api = TradingApi(
        config["networks"][current_network]["dai_eth_price_feed"],
        "weth", 5)
    price = trading_api.getTokenPrice()
    print(price)
    assert price > 0


def test_sell():
    current_network = network.show_active()
    trading_api = TradingApi(
        config["networks"][current_network]["dai_eth_price_feed"],
        "weth", 60 * 2, debug=True)
    to_spend = 0.01 * 10 ** 18

    if trading_api.getBalance()["weth"] < to_spend:
        get_weth(to_spend, trading_api.account.address)

    price = trading_api.getTokenPrice()
    sell_tx = trading_api.sell(to_spend)
    spent, gained = sell_tx.return_value
    assert spent == to_spend and gained >= trading_api.min_amount_scale * 10 ** 18 * to_spend / price


def test_buy():
    current_network = network.show_active()
    trading_api = TradingApi(
        config["networks"][current_network]["dai_eth_price_feed"],
        "weth", 3060 * 2, debug=True)
    buy_for = 10 * 10 ** 18
    price = trading_api.getTokenPrice()

    if trading_api.getBalance()["dai"] < buy_for:
        amount = 1_000 + price * buy_for / 10 ** 18
        get_weth(amount, trading_api.account.address)
        trading_api.sell(amount)

    print(trading_api.getBalance())
    buy_tx = trading_api.buy(buy_for)
    spent, gained = buy_tx.return_value
    assert spent == buy_for and gained >= trading_api.min_amount_scale * price * buy_for / 10 ** 18
