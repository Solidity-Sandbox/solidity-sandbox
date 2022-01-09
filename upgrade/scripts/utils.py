from brownie import network, accounts
from web3 import Web3
import eth_utils

LOCAL_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_ENVIRONENTS = ["eth-mainnet-fork"]


def is_local_env(network):
    return network in LOCAL_ENVIRONMENTS


def is_forked_env(network):
    return network in FORKED_ENVIRONENTS


def get_owner_account():
    current_network = network.show_active()
    if is_local_env(current_network) or is_forked_env(current_network):
        return accounts[0]
    elif current_network == "kovan":
        return accounts.load("test-kovan")
    elif current_network == "rinkeby":
        return accounts.load("test-kovan")


def get_encoded_function(initializer=None, *args):
    if initializer == None:
        return eth_utils.to_bytes(hexstr="0x")

    return initializer.encode_input(*args)
