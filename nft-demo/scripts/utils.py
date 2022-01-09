from brownie import network, accounts, config, LinkToken, VRFCoordinatorMock, Contract
from web3 import Web3

LOCAL_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_ENVIRONENTS = ["eth-mainnet-fork"]

opensea_url = "https://testnets.opensea.io/assets/{}/{}"
BREED_MAPPING = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}


def is_local_env(network):
    return network in LOCAL_ENVIRONMENTS


def is_forked_env(network):
    return network in FORKED_ENVIRONENTS


def get_breed(n):
    return BREED_MAPPING[n]


contract_to_mock = {"link_token": LinkToken, "vrf_coordinator": VRFCoordinatorMock}


def get_contract(contract_name):
    """
    This function will either:
        - Get an address from the config
        - Or deploy a Mock to use for a network that doesn't have the conract

    Args:
        contract_name (string): This is the name of the contract that we will get
        from the config or deploy

    Returns:
        brownie.network.contract.ProjectContract: This is the most recently deployed
        Contract of the type specified by a dictionary. This could either be a mock
        or a 'real' contract on a live network.
    """
    # link_token
    # LinkToken
    contract_type = contract_to_mock[contract_name]
    contract_address = config["networks"][network.show_active()][contract_name]
    contract = Contract.from_abi(
        contract_type._name, contract_address, contract_type.abi
    )
    return contract


def fund_with_link(
    contract_address, account=None, link_token=None, amount=Web3.toWei(0.3, "ether")
):
    account = account if account else get_owner_account()
    link_token = link_token if link_token else get_contract("link_token")
    funding_tx = link_token.transfer(contract_address, amount, {"from": account})
    funding_tx.wait(1)
    print(f"Funded {contract_address}")
    return funding_tx


def get_owner_account():
    current_network = network.show_active()
    if is_local_env(current_network) or is_forked_env(current_network):
        return accounts[0]
    elif current_network == "kovan":
        return accounts.load("test-kovan")
    elif current_network == "rinkeby":
        return accounts.load("test-kovan")
