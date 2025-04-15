// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LearningStorage {
    event NewLearning(address indexed sender, string content);

    string[] public learnings;

    function storeLearning(string memory content) public {
        learnings.push(content);
        emit NewLearning(msg.sender, content);
    }

    function getLearning(uint index) public view returns (string memory) {
        return learnings[index];
    }

    function getTotalLearnings() public view returns (uint) {
        return learnings.length;
    }
}
