// contracts/my_token.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract Dapp_Token is ERC20 {
    constructor(uint256 initialSupply) ERC20("DAPP-STAKE", "DAPP") {
        _mint(msg.sender, initialSupply);
    }
}
