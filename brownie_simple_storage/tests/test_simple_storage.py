from brownie import accounts, SimpleStorage


def test_deploy():
    ## ARRANGE
    owner_account = accounts[0]

    ## ACT
    simple_storage = SimpleStorage.deploy({"from": owner_account})
    starting_value = simple_storage.retrieveN1()
    expected_starting_value = 0

    ## ASSERT
    assert starting_value == expected_starting_value


def test_update():
    ## ARRANGE
    owner_account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": owner_account})

    ## ACT
    expected_value = 15
    simple_storage.storeN1(expected_value, {"from": owner_account})
    updated_value = simple_storage.retrieveN1()

    ## ASSERT
    assert updated_value == expected_value
