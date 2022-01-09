// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract SimpleNFT is ERC721URIStorage {
    uint256 public token_counter;

    constructor() public ERC721("Doggo", "DG") {
        token_counter = 0;
    }

    event doggo_token_id(uint256 new_token_id);

    function adoptDoggo(string memory tokenURI) public returns (uint256) {
        uint256 new_token_id = token_counter;
        _safeMint(msg.sender, new_token_id);
        _setTokenURI(new_token_id, tokenURI);
        token_counter += 1;
        emit doggo_token_id(new_token_id);
        return new_token_id;
    }
}
