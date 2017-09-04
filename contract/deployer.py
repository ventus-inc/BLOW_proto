from web3 import Web3, HTTPProvider, KeepAliveRPCProvider
import sys
import json

args = sys.argv
web3 = Web3(KeepAliveRPCProvider(host='localhost', port='8545'))  # hostとportはgethのデフォルト値
token_binary = args[1] + '.bin'
token_abi = args[1] + '.abi'
binary = open(token_binary)
abi = open(token_abi)
abi = json.loads(abi.read())
cnt = web3.eth.contract()
cnt.bytecode = '0x' + binary.read()
cnt.abi = abi
web3.personal.unlockAccount(web3.eth.coinbase, 'hoge')
cnt.deploy(transaction={'from': web3.eth.coinbase, 'gas': 1000000}, args=(100, 'My', 2, 'test'))
