from brownie import DoggoNFT, config, network
from scripts.utils import get_owner_account
from scripts.create_doggo import get_nft
import os, shutil


def deploy_nft_contract(owner_account):
    print("Re-initializing existing local metadata")
    dir_path = f"./resources/metadata/{network.show_active()}"
    try:
        shutil.rmtree(dir_path)
        print(f"Directory {dir_path} has been removed successfully")
    except OSError as error:
        print(error)
        print(f"Directory {dir_path} can not be removed")
    os.makedirs(dir_path)

    configuration = config["networks"][network.show_active()]
    doggoNFT = DoggoNFT.deploy(
        configuration["vrf_consumer"],
        configuration["link_token"],
        configuration["key_hash"],
        configuration["fee"],
        {"from": owner_account},
    )
    return doggoNFT


def main():
    owner_account = get_owner_account()

    nft_contract = deploy_nft_contract(owner_account)
    # get_nft(nft_contract, owner_account)
