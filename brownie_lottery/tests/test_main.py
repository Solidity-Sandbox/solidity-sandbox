from brownie import Lottery, network, accounts, exceptions

from scripts.deploy import deploy_lottery
from scripts.utils import get_owner_account, is_forked_env, is_local_env
import pytest


def test_everything():
    if not is_local_env(network.show_active()) and not is_forked_env(
        network.show_active()
    ):
        pytest.skip("Only for Development environments")

    owner_account = get_owner_account()
    lottery = deploy_lottery()
    pot = 0
    n_tickets = 0

    with pytest.raises(exceptions.VirtualMachineError):
        lottery.buy_ticket({"from": owner_account})

    entry_value = lottery.start_contest(4000, {"from": owner_account})

    ticket_price = lottery.get_entryFee_inWEI()
    n_tickets += lottery.buy_ticket(
        {"from": owner_account, "value": "{} wei".format(ticket_price)}
    ).events["ticket_bought"]["n_tickets"]
    pot += ticket_price
    assert lottery.get_pot() == pot
    assert len(lottery.get_entrants()) == n_tickets
    assert n_tickets == 1

    n_tickets += lottery.buy_ticket(
        {"from": accounts[1], "value": "{} wei".format(ticket_price)}
    ).events["ticket_bought"]["n_tickets"]
    pot += ticket_price
    assert lottery.get_pot() == pot
    assert len(lottery.get_entrants()) == n_tickets
    assert n_tickets == 2

    n_tickets += lottery.buy_ticket(
        {"from": accounts[2], "value": "{} wei".format(2 * ticket_price)}
    ).events["ticket_bought"]["n_tickets"]
    pot += 2 * ticket_price
    assert lottery.get_pot() == pot
    assert len(lottery.get_entrants()) == n_tickets
    assert n_tickets == 4

    winner = lottery.close_contest({"from": owner_account}).events["contest_closed"][
        "winner"
    ]
    print(winner)
