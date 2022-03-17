# Ethernaut Solutions

Ethernaut is an Etherium smart contract hacking CTF. I didn't see any python solutions online so I decided to create my own.

This project uses python brownie and Web3 frameworks for interacting with the blockchain. I wanted to understand not only how to identify smart contract vulnerabilities, but how to test locally, fork, and interact with testnet.

### How to use this code
1. Download python, brownie, git, etc.
    - Refer to the following 16 hour video/code for how this framework is used for solidity dev 
        - https://www.youtube.com/watch?v=M576WGiDBdQ
        - https://github.com/PatrickAlphaC/brownie_fund_me
2. Set up the configurations
    1. Set the contract addresses within brownie-config.yaml
        - Ethernaut runs on rinkeby. Use the javascript console to run `contract.address` to find your smart contract address. For local testing, we deploy our own contract.
    2. Add a file named `.env` that exports your private environment variables such as PRIVATE_KEY. This can be obtained through metamask.
3. Run the scripts
    - `brownie run scripts/deploy.py --network rinkeby`
    - `brownie run scripts/deploy.py` for development 
        - Test it locally with ganache, set to localhost:8545 to attach to ganache
