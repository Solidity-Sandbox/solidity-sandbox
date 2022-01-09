from brownie import DoggoNFT, config, network
from scripts.utils import get_owner_account, opensea_url, fund_with_link


def get_nft(nft_contract, owner_account):
    fund_with_link(
        nft_contract.address,
        owner_account,
        None,
        config["networks"][network.show_active()]["fee"],
    )
    tx = nft_contract.requestDoggo({"from": owner_account})
    tx.wait(1)
    print("New NFT Has been Created")
    request_id = tx.events["requestBreed"]["request_id"]

    print(f"NFT request with id {request_id} made")


def main():
    owner_account = get_owner_account()
    get_nft(DoggoNFT[-1], owner_account)
