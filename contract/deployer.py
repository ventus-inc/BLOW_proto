from web3 import Web3, HTTPProvider, KeepAliveRPCProvider
import sys
import json
import os

args = sys.argv
cmd = "solc --bin --abi Token.sol -o Token"
os.system(cmd)


def deployer(passphrase):
    web3 = Web3(KeepAliveRPCProvider(host='localhost', port='8545'))
    token_binary = 'Token/FixedSupplyToken.bin'
    token_abi = 'Token/FixedSupplyToken.abi'
    binary = open(token_binary)
    abi = open(token_abi)
    abi = json.loads(abi.read())
    cnt = web3.eth.contract()
    cnt.bytecode = '0x' + binary.read()
    cnt.abi = abi
    web3.personal.unlockAccount(web3.eth.coinbase, passphrase)  # pass phrase
    a = cnt.deploy(transaction={'from': web3.eth.coinbase, 'gas': 1000000})

deployer(args[1])