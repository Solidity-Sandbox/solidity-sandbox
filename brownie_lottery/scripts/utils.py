from brownie import MockV3Aggregator, network, accounts, config

MOCKV3_DECIMALS = 8
MOCKV3_STARTING_PRICE = 3800 * (10 ** 8)
LOCAL_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_ENVIRONENTS = ["eth-mainnet-fork"]


def is_local_env(network):
    return network in LOCAL_ENVIRONMENTS


def is_forked_env(network):
    return network in FORKED_ENVIRONENTS


def deploy_Mock_V3(owner_account):
    if len(MockV3Aggregator) <= 0:
        print("DEPLOYING MOCK AGGREGATOR")
        MockV3Aggregator.deploy(
            MOCKV3_DECIMALS, MOCKV3_STARTING_PRICE, {"from": owner_account}
        )
    return MockV3Aggregator[-1]


def get_owner_account():
    current_network = network.show_active()
    if is_local_env(current_network) or is_forked_env(current_network):
        return accounts[0]
    elif current_network == "kovan":
        return accounts.load("test-kovan")
