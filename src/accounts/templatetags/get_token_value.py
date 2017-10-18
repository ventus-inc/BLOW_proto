from django import template
from django.contrib.auth import get_user_model
from web3 import Web3, HTTPProvider, KeepAliveRPCProvider
from tokens.models import Token
import json
from accounts.models import UserProfile

register = template.Library()

User = get_user_model()


@register.filter()
def get_token_value(value):
    web3 = Web3(KeepAliveRPCProvider(host='localhost', port='8545'))
    web3.personal.unlockAccount(User.profile.wallet.num, User.profile.username)
    f = open("transactions/abi.json", 'r')
    abi = json.loads(f.read())
    """
    for token_user in User.profile.have_token.all():
        cnt = web3.eth.contract(abi, token_user.token_address)
        tokenlot = cnt.call().balanceOf(User.wallet.num)
        print("----------------")
        print(token_user.username)
        print(tokenlot)
        print("----------------")
    # print(tokenlot)
    """
    return 0
