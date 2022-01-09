// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract DoggoNFT is ERC721URIStorage, VRFConsumerBase {
    uint256 public token_counter;
    bytes32 public keyHash;
    uint256 public fee;
    enum Breed {
        PUG,
        SHIBA_INU,
        ST_BERNARD
    }
    mapping(uint256 => Breed) public token_to_breed;
    mapping(bytes32 => address) public requestID_to_sender;

    constructor(
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyHash,
        uint256 _fee
    )
        public
        VRFConsumerBase(_vrfCoordinator, _linkToken)
        ERC721("Doggo", "DG")
    {
        token_counter = 0;
        keyHash = _keyHash;
        fee = _fee;
    }

    event doggo_token_id(uint256 new_token_id);
    event requestBreed(bytes32 indexed request_id, address sender);
    event breedAssigned(uint256 indexed token_id, Breed breed);
    event set_token_uri(uint256 token_id, string _token_uri);

    function fulfillRandomness(bytes32 requestId, uint256 randomness)
        internal
        override
    {
        Breed breed = Breed(randomness % 3);
        uint256 new_token_id = token_counter;
        token_to_breed[new_token_id] = breed;
        emit breedAssigned(new_token_id, breed);

        _safeMint(requestID_to_sender[requestId], new_token_id);
        //_setTokenURI(new_token_id, tokenURI);
        token_counter += 1;
    }

    function requestDoggo() public returns (bytes32) {
        require(
            LINK.balanceOf(msg.sender) >= fee,
            "Not enough LINK - fill contract with faucet"
        );

        bytes32 vrf_request_id = requestRandomness(keyHash, fee);
        requestID_to_sender[vrf_request_id] = msg.sender;
        emit requestBreed(vrf_request_id, msg.sender);
        return vrf_request_id;
    }

    function setTokenURI(uint256 token_id, string memory _token_uri) public {
        require(
            _isApprovedOrOwner(_msgSender(), token_id),
            "ERC721: Caller neither owner nor approved"
        );
        emit set_token_uri(token_id, _token_uri);
        _setTokenURI(token_id, _token_uri);
    }
}
