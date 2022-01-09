from brownie import FundMe, MockV3Aggregator, network, config
from scripts.utils import get_account, deploy_mock_aggregator, is_local_environment


def deploy_contract():
    ## Account Details
    owner_account = get_account()

    print("Owner Account Address : {}".format(owner_account))

    ## Deploy
    if is_local_environment(network.show_active()):
        print("DEVELOPMENT NETWORK")
        deploy_mock_aggregator(owner_account)
        pricefeedAddress = MockV3Aggregator[-1].address
    else:
        pricefeedAddress = config["eth_usd_price_feeds"][network.show_active()][
            "pricefeedAddress"
        ]

    fund_me = FundMe.deploy(pricefeedAddress, {"from": owner_account})
    return fund_me


def main():
    deploy_contract()
