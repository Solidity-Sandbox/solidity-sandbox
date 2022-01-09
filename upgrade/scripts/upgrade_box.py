from brownie.network.contract import Contract
from scripts.utils import get_owner_account, get_encoded_function
from brownie import Box, BoxV2, TransparentUpgradeableProxy, ProxyAdmin


def deploy(owner_account):
    box = Box.deploy({"from": owner_account})

    proxy_admin = ProxyAdmin.deploy({"from": owner_account})

    box_encoded_initializer = get_encoded_function(box.setValue, 1)

    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer,
        {"from": owner_account},
    )

    return proxy


def upgrade(proxy, proxy_admin, owner_account):
    box_v2 = BoxV2.deploy({"from": owner_account})
    proxy_admin.upgrade(proxy, box_v2.address)


def main():
    owner_account = get_owner_account()

    deploy(owner_account)
    proxy_admin = ProxyAdmin[-1]
    proxy = TransparentUpgradeableProxy[-1]
    print(f"Proxy at {proxy.address}")

    box_proxy = Contract.from_abi("Box", proxy.address, Box.abi)
    print(f"Initial V1 Value: {box_proxy.getValue()}")
    tx = box_proxy.setValue(10, {"from": owner_account})
    tx.wait(1)
    print(f"Final V1 Value: {box_proxy.getValue()}")

    upgrade(proxy, proxy_admin, owner_account)
    box_proxy = Contract.from_abi("Box", proxy.address, BoxV2.abi)
    print(f"Initial V2 Value: {box_proxy.getValue()}")
    tx = box_proxy.setValue(100, {"from": owner_account})
    tx.wait(1)
    print(f"New V2 Value: {box_proxy.getValue()}")

    tx = box_proxy.increment({"from": owner_account})
    tx.wait(1)
    print(f"Final V2 Value: {box_proxy.getValue()}")
