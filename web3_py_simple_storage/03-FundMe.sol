// SPDX-License-Identifier: GPL-3.0

pragma solidity 0.6.7;

// import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    modifier onlyOwner() {
        require(msg.sender == owner, "UNAUTHORIZED TRANSACTION");
        _;
    }

    mapping(address => uint256) public addr2Funded;
    mapping(address => uint256) public addr2Balance;
    address[] public addrArray;
    address public owner;

    constructor() public {
        owner = msg.sender;
    }

    function fund() public payable {
        //uint256 minimumInvestment = 1 * (10**18);//10 usd
        //require(minimumInvestment <= getWEIAmounttoUSD(msg.value), "GIMME MORE MONEY!");
        require(msg.value > 0, "YOU CHEAPSTAKE!!!");
        if (addr2Balance[msg.sender] == 0) {
            addrArray.push(msg.sender);
        }
        addr2Funded[msg.sender] += msg.value;
        addr2Balance[msg.sender] += msg.value;
    }

    function withdraw() public onlyOwner {
        msg.sender.transfer(address(this).balance);
        for (
            uint256 funderIndex = 0;
            funderIndex < addrArray.length;
            funderIndex++
        ) {
            addr2Balance[addrArray[funderIndex]] = 0;
        }
        delete addrArray;
    }

    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }

    /*    
    function getVersion() public view returns(uint256) {
        return AggregatorV3Interface(0x9326BFA02ADD2366b30bacB125260Af641031331).version();
    }
    
    //Returns 1 eth in usd * (10 ** 18)
    function getWEIinUSD() public view returns(uint256) {
        ( , int256 value, , ,) = AggregatorV3Interface(0x9326BFA02ADD2366b30bacB125260Af641031331).latestRoundData();
        return uint256(value * (10**10));
    }
    
    function getWEIAmounttoUSD(uint256 amount) public view returns(uint256) {
        return getWEIinUSD() * amount / (10**18);
    }
*/
}
