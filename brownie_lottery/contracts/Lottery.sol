// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Lottery {
    address[] private entrants;
    address private owner;
    uint256 private entryFee;
    uint256 private entryFee_inWEI;
    uint256 private pot;
    AggregatorV3Interface private priceFeed;
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }

    LOTTERY_STATE public lottery_state;

    constructor(address _priceFeedAddress) public {
        owner = msg.sender;
        priceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function get_entryFee() public view returns (uint256) {
        return entryFee;
    }

    function get_entryFee_inWEI() public view returns (uint256) {
        return USDToWEI(entryFee);
    }

    function get_owner() public view onlyOwner returns (address) {
        return owner;
    }

    function get_entrants() public view returns (address[] memory) {
        return entrants;
    }

    function get_pot() public view returns (uint256) {
        return pot;
    }

    function oneUSDToWEI() public view returns (uint256) {
        (, int256 value, , , ) = priceFeed.latestRoundData();
        return uint256((10**26) / value);
    }

    function USDToWEI(uint256 amount) public view returns (uint256) {
        return amount * oneUSDToWEI();
    }

    function getPRN(
        uint256 seed,
        uint256 salt,
        uint256 sugar
    ) public view returns (uint8) {
        bytes32 bHash = blockhash(block.number - 1);
        uint8 randomNumber = uint8(
            uint256(
                keccak256(
                    abi.encodePacked(block.timestamp, bHash, seed, salt, sugar)
                )
            ) % seed
        );
        return randomNumber;
    }

    function start_contest(uint256 new_entry_fee) public onlyOwner {
        require(new_entry_fee > 0, "CAN'T SET NON-ZERO ENTRY FEE");
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            "LOTTERY ALREADY IN PROGRESS..."
        );
        entryFee = new_entry_fee;
        lottery_state = LOTTERY_STATE.OPEN;
    }

    event ticket_bought(address buyer, uint256 n_tickets);

    function buy_ticket() public payable {
        pot += msg.value;
        require(
            lottery_state == LOTTERY_STATE.OPEN,
            "LOTTERY NOT STARTED YET..."
        );
        require(
            msg.value >= get_entryFee_inWEI(),
            "NOT ENOUGH AMOUNT FUNDED..."
        );
        uint256 n_tickets = msg.value / get_entryFee_inWEI();
        for (uint256 i = 1; i <= n_tickets; i++) {
            entrants.push(msg.sender);
        }
        emit ticket_bought(msg.sender, n_tickets);
    }

    event contest_closed(address winner, uint256 prize);

    function close_contest() public payable onlyOwner {
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        uint8 winner_index = getPRN(entrants.length, 342, 2);
        msg.sender.transfer(address(this).balance / 5);
        uint256 prize = address(this).balance;
        address payable winner = payable(entrants[winner_index]);
        winner.transfer(address(this).balance);
        pot = 0;
        lottery_state = LOTTERY_STATE.CLOSED;
        emit contest_closed(winner, prize);
    }
}
