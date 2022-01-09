from brownie import accounts, SimpleStorage, network


def read_contract():
    simple_storage = SimpleStorage[-1]
    print(simple_storage.retrieveN1())


def main():
    read_contract()
