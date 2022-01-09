pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";

contract Token_Farm is Ownable {
    //send token
    //withdraw token
    //approve
    //view value
    //issue Dapp token
    address[] public allowed_tokens;

    constructor() public {}

    function addAllowedToken(address token_address) public {}

    function tokenIsAllowed(address token_address) public view returns (bool) {
        for (uint256 index = 0; index < allowed_tokens.length; index++) {
            if (allowed_tokens[index] == token_address) {
                return true;
            }
        }
        return false;
    }

    function stakeToken(uint256 amount, address token_address) public {
        require(amount > 0);
        require(tokenIsAllowed(token_address));
    }
}
