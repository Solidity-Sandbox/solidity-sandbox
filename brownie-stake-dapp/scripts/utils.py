from brownie import network, accounts, config

MOCKV3_DECIMALS = 8
MOCKV3_STARTING_PRICE = 3800 * (10 ** 8)
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
        return accounts.load("kovan")
