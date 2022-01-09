from scripts.utils import get_owner_account, get_abi_dictionary
from brownie import config, network, Contract
from web3 import Web3


def get_weth(owner_account, amount):
    # Mints eth to weth by caling contract, using
    ## ABI
    ## Contract Address
    # weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    weth = Contract.from_abi(
        "Weth",
        config["networks"][network.show_active()]["weth_token"],
        get_abi_dictionary("weth"),
    )
    tx = weth.deposit({"from": owner_account, "value": amount})
    print("Received {} wei".format(amount))
    return tx


def main():
    owner_account = get_owner_account()
    amount = Web3.toWei(0.1, "ether")
    get_weth(owner_account, amount)
