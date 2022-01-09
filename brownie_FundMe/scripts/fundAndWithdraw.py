from brownie import FundMe
from brownie.network import account
from scripts.utils import get_account

fund_me = FundMe[-1]
account = get_account()


def get_entrance_fee():
    entrance_fee = fund_me.getEntranceFee()
    return entrance_fee


def entry_fund():
    entrance_fee = get_entrance_fee()
    print("Entrance Fee: {}".format(entrance_fee))
    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw_funds():
    fund_me.withdraw({"from": account})


def main():
    print("1: Enter Funds\n2: Withdraw Funds")
    choice = 2
    if choice == 1:
        entry_fund()
    elif choice == 2:
        withdraw_funds()
    else:
        print("INVALID INPUT")
