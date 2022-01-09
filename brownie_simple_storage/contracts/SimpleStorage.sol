// SPDX-License-Identifier: GPL-3.0

pragma solidity 0.8.7;

contract SimpleStorage {
    int256 n1;

    struct Person {
        uint256 balance;
        string name;
    }

    Person[] public people;
    mapping(string => uint256) public balance2Name;

    function newPerson(uint256 _balance, string memory _name) public {
        people.push(Person({balance: _balance, name: _name}));
        balance2Name[_name] = _balance;
    }

    function storeN1(int256 _n1) public returns (bool) {
        n1 = _n1;
        return true;
    }

    function retrieveN1() public view returns (int256) {
        return n1;
    }
}
