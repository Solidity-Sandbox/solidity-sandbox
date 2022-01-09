// SPDX-License-Identifier: GPL-3.0

pragma solidity 0.8.7;

import "./01-SimpleStorage.sol";

contract StorageFactory is SimpleStorage {
    SimpleStorage[] public simpleStorageArray;

    function createSimpleStorageContract() public {
        SimpleStorage simpleStorage = new SimpleStorage();
        simpleStorageArray.push(simpleStorage);
    }

    function simpleStoreN1(uint256 storageIndex, int256 value) public {
        simpleStorageArray[storageIndex].storeN1(value);
    }

    function simpleRetrieveN1(uint256 storageIndex)
        public
        view
        returns (int256)
    {
        return simpleStorageArray[storageIndex].retrieveN1();
    }
}
