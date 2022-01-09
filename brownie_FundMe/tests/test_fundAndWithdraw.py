import brownie
from scripts.utils import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_contract
from brownie import network, accounts, exceptions
import pytest


def test_generalFundAndWithdraw():
    ## ARRANGE
    account = get_account()
    fund_me = deploy_contract()
    entrance_fee = fund_me.getEntranceFee()

    ## ACT 1
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    # tx.wait(1)
    ## ASSERT 1
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee

    ## ACT 2
    tx = fund_me.withdraw({"from": account})
    # tx.wait(1)
    ## ASSERT 2
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_onlyOwnerWithdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("ONLY FOR LOCAL TESTING")

    ## ARRANGE
    fund_me = deploy_contract()
    bad_actor = accounts[1]
    print("BAD ACTOR: {}".format(bad_actor))

    ## ACT / ASSERT
    with pytest.raises(ValueError):
        tx = fund_me.withdraw({"from": bad_actor})
