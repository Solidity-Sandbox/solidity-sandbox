from brownie.network.contract import Contract
from scripts.utils import get_owner_account, get_encoded_function
from brownie import Box, TransparentUpgradeableProxy, ProxyAdmin


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


def main():
    owner_account = get_owner_account()
    proxy = deploy(owner_account)
    box_proxy = Contract.from_abi("Box", proxy.address, Box.abi, None)
    print(box_proxy.getValue())
    tx = box_proxy.setValue(5, {"from": owner_account})
    tx.wait(1)
    print(box_proxy.getValue())
