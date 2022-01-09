from brownie import Lottery, config, network
from scripts.utils import is_local_env, is_forked_env, deploy_Mock_V3, get_owner_account


def deploy_lottery():
    owner_account = get_owner_account()
    current_network = network.show_active()
    if is_local_env(current_network):
        pricefeedAddress = deploy_Mock_V3(owner_account).address
    else:
        pricefeedAddress = config["eth_usd_price_feeds"][current_network][
            "pricefeedAddress"
        ]
    lottery = Lottery.deploy(pricefeedAddress, {"from": owner_account})
    return lottery


def main():
    deploy_lottery()
