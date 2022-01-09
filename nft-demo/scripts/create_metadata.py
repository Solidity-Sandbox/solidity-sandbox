from brownie import DoggoNFT, network, config
from scripts.utils import get_breed
from resources.metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json

breed_to_ipfs = {
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png",
}


def pin_pinata(file_path):
    with Path(file_path).open("rb") as fp:
        file_binary = fp.read()
        pinata_config = config["pinata"]
        base_url = pinata_config["url"]
        api_endpoint = "/pinning/pinFileToIPFS"
        headers = {
            "pinata_api_key": pinata_config["api_key"],
            "pinata_secret_api_key": pinata_config["api_secret"],
        }
        response = requests.post(
            f"{base_url}{api_endpoint}", headers=headers, files={"file": file_binary}
        )
        pinataHash = response.json()["IpfsHash"]
        filename = file_path.split("/")[-1]
        file_uri = f"https://ipfs.io/ipfs/{pinataHash}?filename={filename}"
        print(f"Pinned {filename} to pinata ipfs nodes.")
        print(f"URL: {file_uri}")
        return file_uri


def upload_to_ipfs(file_path):
    with Path(file_path).open("rb") as fp:
        file_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        api_endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + api_endpoint, files={"file": file_binary})
        ipfs_hash = response.json()["Hash"]
        filename = file_path.split("/")[-1]
        file_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(f"Uploaded {file_uri}")
        return file_uri


def generate_metadata():
    pass


def main():
    doggoNFT = DoggoNFT[-1]
    number_of_collectibles = doggoNFT.token_counter()
    print(f"You have create {number_of_collectibles} collectibles.")
    for token_id in range(number_of_collectibles):
        breed = get_breed(doggoNFT.token_to_breed(token_id))
        metadata_file_path = (
            f"./resources/metadata/{network.show_active()}/{token_id}-{breed}.json"
        )

        collectible_metadata = dict(metadata_template)
        if Path(metadata_file_path).exists():
            print(f"{metadata_file_path} already exists!")
        else:
            print(f"Creating {metadata_file_path}...")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed} doggo!!"

            breed_image_name = str(breed).replace("_", "-").lower()
            image_file_path = f"./resources/images/{breed_image_name}.png"

            if breed not in breed_to_ipfs:
                breed_to_ipfs[breed] = pin_pinata(image_file_path)
            image_uri = breed_to_ipfs[breed]

            collectible_metadata["image"] = image_uri

            with open(metadata_file_path, "w") as md_fp:
                json.dump(collectible_metadata, md_fp, indent=4)
