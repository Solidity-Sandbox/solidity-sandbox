from brownie import interface, config, network
from scripts.utils import (
    is_forked_env,
    get_owner_account,
    get_borrowable_data,
    get_asset_price,
)
from scripts.get_weth import get_weth
from web3 import Web3


def get_lending_pool():
    lending_pool_address = interface.LendingPoolAddressesProvider(
        config["networks"][network.show_active()][
            "aave_lending_pool_addresses_provider"
        ]
    ).getLendingPool()
    print(f"Lending Pool Contract Address: {lending_pool_address}")
    return interface.LendingPool(lending_pool_address)


def approve_erc20(amount, spender, erc20_address, account):
    print(f"Approving ERC20 token {amount} of address {erc20_address}...")
    erc20 = interface.ERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved!!")


def repay_all(lending_pool, asset_address, debt_amount, owner_account):
    approve_erc20(
        debt_amount,
        lending_pool.address,
        asset_address,
        owner_account,
    )
    tx = lending_pool.repay(
        asset_address,
        debt_amount,
        2,
        owner_account.address,
        {"from": owner_account},
    )
    tx.wait(1)


def get_erc20_balance(erc20_address, owner_account):
    erc20 = interface.ERC20(erc20_address)
    return erc20.balanceOf(owner_account)


def deposit_collateral(lending_pool, erc20_address, amount, owner_account):
    tx = lending_pool.deposit(
        erc20_address, amount, owner_account.address, 0, {"from": owner_account}
    )
    tx.wait(1)
    print("Deposited")


def main():
    network.gas_limit(100000)
    amount = Web3.toWei(0.1, "ether")
    owner_account = get_owner_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if is_forked_env(network.show_active()):
        get_weth(owner_account, amount)
    lending_pool = get_lending_pool()

    """
    approve_erc20(
        amount,
        lending_pool.address,
        erc20_address,
        owner_account,
    )
    """

    # deposit_collateral(lending_pool, lending_pool, erc20_address, amount, owner_account)

    availableBorrowsETH = get_borrowable_data(owner_account, lending_pool)[2]

    print("Lets Borrow DAI!!")
    dai_to_eth_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )

    print(f"Price of 1 DAI: {dai_to_eth_price} eth")

    amount_dai_to_borrow = 0.50 * availableBorrowsETH / dai_to_eth_price
    print(f"Trying to borrow {amount_dai_to_borrow} DAI")

    tx = lending_pool.borrow(
        config["networks"][network.show_active()]["dai_token"],
        Web3.toWei(amount_dai_to_borrow, "ether"),
        2,
        0,
        owner_account,
        {"from": owner_account},
    )
    tx.wait(1)

    print(
        f"Successfully borrowed {amount_dai_to_borrow} DAI\n\nCurrent Account State:\n"
    )

    debt_amount = get_borrowable_data(owner_account, lending_pool)[1]

    dai_balance = get_erc20_balance(
        config["networks"][network.show_active()]["dai_token"], owner_account
    )
    print(f"Current DAI in account {dai_balance}")

    print(f"Now Repaying {dai_balance} DAI")
    repay_all(
        lending_pool,
        config["networks"][network.show_active()]["dai_token"],
        dai_balance,
        owner_account,
    )

    print("Account State after repayment")
    get_borrowable_data(owner_account, lending_pool)
