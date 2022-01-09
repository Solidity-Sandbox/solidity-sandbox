from brownie import My_Token, network
from scripts.utils import get_owner_account
from web3 import Web3


def deploy_my_token():
    owner_account = get_owner_account()
    print(owner_account)
    My_Token.deploy(Web3.toWei(1000, "ether"), {"from": owner_account})
    return My_Token[-1]


def main():
    deploy_my_token()
