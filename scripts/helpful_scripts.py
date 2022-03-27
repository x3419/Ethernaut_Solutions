from brownie import network, config, accounts, MockV3Aggregator, Contract
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev", "rinkeby-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

DECIMALS = 8
STARTING_PRICE = 200000000000


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        #or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
    print("Mocks Deployed!")


def deploy_contract(ContractClass, className, localAccountIndex, localConstructorArgs):
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:# or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        if len(localConstructorArgs) > 0:
            classInstance = ContractClass.deploy(*localConstructorArgs, {"from": accounts[localAccountIndex]}, publish_source=False)
        else:
            classInstance = ContractClass.deploy({"from": accounts[localAccountIndex]}, publish_source=False)
    else: # either testnet or fork
        classInstanceAddress = config["networks"][network.show_active()][f"{className}_address"]
        classInstance = Contract.from_abi(className, classInstanceAddress, ContractClass.abi)

    return classInstance