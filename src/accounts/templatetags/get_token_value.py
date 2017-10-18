from django import template
from django.contrib.auth import get_user_model
from web3 import Web3, HTTPProvider, KeepAliveRPCProvider
from tokens.models import Token
import json
from accounts.models import UserProfile

register = template.Library()

User = get_user_model()


@register.filter()
def get_token_value(touser,fromuser):
    web3 = Web3(KeepAliveRPCProvider(host='localhost', port='8545'))
    #web3.personal.unlockAccount(touser.wallet.num, fromuser.username)
    print(fromuser.username)
    #web3.personal.unlockAccount(fromuser.wallet.num, fromuser.username)
    f = open("transactions/abi.json", 'r')
    abi = json.loads(f.read())
    cnt = web3.eth.contract(abi, touser.profile.token_address)
    tokenlot = cnt.call().balanceOf(fromuser.wallet.num)
    #f = open("transactions/abi.json", 'r')
    #abi = json.loads(f.read())

    return tokenlot