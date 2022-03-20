# Ethernaut Solutions

Ethernaut is an Ethereum smart contract hacking CTF. I didn't see any python solutions online so I decided to create my own.

This project uses python brownie and Web3 frameworks for interacting with the blockchain. I wanted to understand not only how to identify smart contract vulnerabilities, but how to test locally, fork, and interact with testnet seamlessly depending on the network specified through brownie. 

### How to use this code
1. Download python, brownie, ganache, ganache-cli, etc.
    - Refer to the following 16 hour video/code on how this framework is used for solidity dev 
        - https://www.youtube.com/watch?v=M576WGiDBdQ
        - https://github.com/PatrickAlphaC/brownie_fund_me
        - https://github.com/PatrickAlphaC/smartcontract-lottery
2. Set up the configurations
    1. Set the contract addresses within brownie-config.yaml
        - Ethernaut runs on rinkeby. Use the javascript console to run `contract.address` to find your smart contract address. For local testing, we deploy our own contract.
    2. Add a file named `.env` that exports your private environment variables such as PRIVATE_KEY. This can be obtained through metamask.
        - `export PRIVATE_KEY=asdf`
        - `export WEB3_INFURA_PROJECT_ID=asdf`
        - `export WEB3_INFURA_API_SECRET=asdf`
        
3. Run the scripts
    - `brownie run scripts/deploy.py --network rinkeby`
    - `brownie run scripts/deploy.py` for development 
        - Test it locally with ganache, set to localhost:8545 to attach to ganache

For some challenges I've added fork testing functionality. This is an important topic that I wanted to learn so I've implemented it where it makes sense.
- Ex) For `Token` the `player` automatically receives 20 tokens and the initialSize is unknown as we didn't deploy the contract. Through local testing we can deploy and send ourselves 20 tokens using `transfer`, but we're having to guess the commands used for deployment. Forking allows us to grab the relevant addresses and interact with the EVM in its current state on the blockchain. 

To fork with brownie use the following command:
`brownie networks add development rinkeby-fork-dev cmd=ganache-cli host=http://127.0.0.1 fork='https://rinkeby.infura.io/v3/{INFURA_ID}' accounts=10 mnemonic=brownie port=8545`
Then
`brownie run scripts/deploy.py --network rinkeby-fork-dev`