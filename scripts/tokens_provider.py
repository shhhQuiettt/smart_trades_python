from brownie import config, interface, network


def get_weth(amount, to_address):
    current_network = network.show_active()
    weth_contract = interface.IWethLike(config["networks"][current_network]["token"]["weth"])
    tx = weth_contract.deposit({"from": to_address, "value": amount})
    tx.wait(1)
    return tx
