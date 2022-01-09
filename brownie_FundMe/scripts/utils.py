from brownie import accounts, FundMe, MockV3Aggregator, network, config
from web3 import Web3

DECIMALS = 8
STARTING_PRICE = 2000 * (10 ** 8)
FORKED_BLOCKCHAIN_ENVIRONMENTS = ["eth-mainnet-fork"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account():
    if is_local_environment(network.show_active()) or is_forked_environment(
        network.show_active()
    ):
        return accounts[0]
    elif network.show_active() == "kovan":
        account = accounts.load("test-kovan")
        return account


def deploy_mock_aggregator(owner_account):
    if len(MockV3Aggregator) <= 0:
        print("DEPLOYING MOCK AGGREGATOR")
        mock_v3 = MockV3Aggregator.deploy(
            DECIMALS, STARTING_PRICE, {"from": owner_account}
        )


def is_local_environment(env_name):
    return env_name in LOCAL_BLOCKCHAIN_ENVIRONMENTS


def is_forked_environment(env_name):
    return env_name in FORKED_BLOCKCHAIN_ENVIRONMENTS
