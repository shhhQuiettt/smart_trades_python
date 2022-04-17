from scripts.trading.TradingApi import TradingApi
from brownie import network, config

current_network = network.show_active()
trading_api = TradingApi(config["networks"][current_network]["dai_eth_price_feed"], "weth", 60 * 2)
price = trading_api.getTokenPrice()
print(f"weth balance {confg['networks'][current_network]['token']["weth]}")
spent, received = trading_api.buy(1000)
