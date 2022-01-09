from brownie import SimpleNFT, network
from scripts.utils import get_owner_account, opensea_url

sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"


def deploy_nft_contract(owner_account):
    simpleNFT = SimpleNFT.deploy({"from": owner_account})
    return simpleNFT


def get_nft(nft_contract, owner_account):
    tx = nft_contract.adoptDoggo(sample_token_uri, {"from": owner_account})
    tx.wait(1)
    token_id = tx.events["doggo_token_id"]["new_token_id"]
    print(
        f"You may view your NFT at {opensea_url.format(nft_contract.address, token_id)}"
    )


def main():
    owner_account = get_owner_account()

    nft_contract = deploy_nft_contract(owner_account)
    get_nft(nft_contract, owner_account)
