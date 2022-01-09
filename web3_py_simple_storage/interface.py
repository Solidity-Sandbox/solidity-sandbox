from solcx import compile_standard
from solcx import install_solc
import json
from web3 import Web3

install_solc("0.8.7")

## Transactor's Info
# my_address = "0xdaCdBb945D543fe1D31c9B0917E24b395faCd293"
# private_key = "0x803b79bb97a3fae6120ab7ba1ead27221ae8ef14748372e7987f6364196acbf9"

my_address = "0xfAd0c5551519961Af800916616A273314740E2c1"
private_key = "0x07ba1f6174225ffe970a1ed309a28103e72ebffd81168aaf6ca26143a11e7488"

## Reading Contract Details
with open("compiled_json.json") as solFile:
    contract_data = json.load(solFile)

with open("contract_address.txt") as addrFile:
    contract_address = addrFile.read()

## Parse Contract Details
contract_name = list(contract_data["contracts"].keys())[0]
print("Contract: {} at address: {}".format(contract_name, contract_address))
abi = contract_data["contracts"][contract_name]["SimpleStorage"]["abi"]

## Establishing Connection
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chainId = 1337
contract_obj = w3.eth.contract(address=contract_address, abi=abi)

## Retrieves/Transactions

print(contract_obj.functions.retrieveN1().call())

store_transaction = contract_obj.functions.storeN1(25).buildTransaction(
    {
        "chainId": chainId,
        "from": my_address,
        "nonce": w3.eth.getTransactionCount(my_address),
    }
)
signed_transaction = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
txn_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
