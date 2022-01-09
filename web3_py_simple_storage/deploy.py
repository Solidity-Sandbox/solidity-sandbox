from solcx import compile_standard
from solcx import install_solc
import json
from web3 import Web3

install_solc("0.8.7")

contract_source = "01-SimpleStorage.sol"
with open(contract_source) as solFile:
    solFileData = solFile.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {contract_source: {"content": solFileData}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.7",
)

## Contract Compiled Outputs
with open("compiled_json.json", "w") as dumpFile:
    json.dump(compiled_sol, dumpFile, indent=4)

bytecode = compiled_sol["contracts"][contract_source]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]
abi = compiled_sol["contracts"][contract_source]["SimpleStorage"]["abi"]

with open("abi.json", "w") as dumpFile:
    json.dump(abi, dumpFile, indent=4)

## Connection
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chainId = 1337
owner_address = "0xdaCdBb945D543fe1D31c9B0917E24b395faCd293"
private_key = "0x803b79bb97a3fae6120ab7ba1ead27221ae8ef14748372e7987f6364196acbf9"

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = w3.eth.getTransactionCount(owner_address)

transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chainId, "from": owner_address, "nonce": nonce}
)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

transaction_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

print(tx_receipt)
print(type(tx_receipt))

with open("contract_address.txt", "w") as dumpFile:
    dumpFile.writelines(tx_receipt.contractAddress)
