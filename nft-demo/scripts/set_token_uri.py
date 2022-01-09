from brownie import DoggoNFT, network
from scripts.utils import get_breed, get_owner_account, opensea_url

dog_metadata_dict = {
    "PUG": "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmdryoExpgEQQQgJPoruwGJyZmz6SqV4FRTX1i73CT3iXn?filename=1-SHIBA_INU.json",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmbBnUjyHHN7Ytq9xDsYF9sucZdDJLRkWz7vnZfrjMXMxs?filename=2-ST_BERNARD.json",
}


def set_tokenURI(nft_contract, owner_account, token_id, token_uri):
    print(f"Setting Token URI to {token_uri}")
    tx = nft_contract.setTokenURI(token_id, token_uri, {"from": owner_account})
    tx.wait(1)
    nft_url = opensea_url.format(nft_contract.address, token_id)
    print(f"Great!! You can see your NFT at {nft_url}")


def main():
    current_network = network.show_active()
    owner_account = get_owner_account()
    print(f"Currently on network {current_network}")
    doggoNFT = DoggoNFT[-1]
    number_of_collectibles = doggoNFT.token_counter()
    print(f"You have created {number_of_collectibles} collectibles.")
    for token_id in range(number_of_collectibles):
        breed = get_breed(doggoNFT.token_to_breed(token_id))
        token_uri = doggoNFT.tokenURI(token_id)
        if token_uri.startswith("https://"):
            print(f"Token URI Already Set to {token_uri}")
            continue
        if breed in dog_metadata_dict:
            token_uri = dog_metadata_dict[breed]
        set_tokenURI(doggoNFT, owner_account, token_id, token_uri)
