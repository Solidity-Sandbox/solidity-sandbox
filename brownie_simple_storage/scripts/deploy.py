from brownie import accounts, SimpleStorage, network


def get_account():
    if network.show_active() == "development":
        return [accounts[0], accounts[1]]
    elif network.show_active() == "kovan":
        account = accounts.load("test-kovan")
        return [account, account]


def deploy_contract():
    ## Account Details
    # owner_account = accounts[0]
    # txn_account = accounts[1]
    (owner_account, txn_account) = get_account()

    print("Owner Account Address : {}".format(owner_account))
    print("Transaction Account Address : {}".format(txn_account))

    ## Deploy
    simple_storage = SimpleStorage.deploy({"from": owner_account})

    stored_value = simple_storage.retrieveN1()
    print("Initial Value: {}".format(stored_value))

    transtaction = simple_storage.storeN1(24, {"from": txn_account})

    stored_value = simple_storage.retrieveN1()
    print("Updated Value: {}".format(stored_value))


def main():
    deploy_contract()
