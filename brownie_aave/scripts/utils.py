from brownie import MockV3Aggregator, network, accounts, config, interface
import json
from web3 import Web3

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


def get_borrowable_data(owner_account, lending_pool):
    (
        totalCollateralETH,
        totalDebtETH,
        availableBorrowsETH,
        currentLiquidationThreshold,
        ltv,
        healthFactor,
    ) = lending_pool.getUserAccountData(owner_account)
    totalCollateralETH = float(Web3.fromWei(totalCollateralETH, "ether"))
    totalDebtETH = float(Web3.fromWei(totalDebtETH, "ether"))
    availableBorrowsETH = float(Web3.fromWei(availableBorrowsETH, "ether"))
    print("You have {} eth total collateral".format(totalCollateralETH))
    print("You have {} eth total debt".format(totalDebtETH))
    print("You have {} total eth to borrow".format(availableBorrowsETH))
    return (
        totalCollateralETH,
        totalDebtETH,
        availableBorrowsETH,
        currentLiquidationThreshold,
        ltv,
        healthFactor,
    )


def get_asset_price(price_feed_address):
    price_feed = interface.AggregatorV3(price_feed_address)
    return float(Web3.fromWei(price_feed.latestRoundData()[1], "ether"))


def get_owner_account():
    current_network = network.show_active()
    if is_local_env(current_network) or is_forked_env(current_network):
        return accounts[0]
    elif current_network == "kovan":
        return accounts.load("test-kovan")


def get_abi_dictionary(name):
    with open("interfaces/abi_{}.json".format(name), "r") as json_file:
        return json.load(json_file)


def get_lending_pool_address_provider():
    interface.ILendingPoolAddressesProvider()
