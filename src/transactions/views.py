from django.views.generic.edit import FormView
from web3 import Web3,formatters,KeepAliveRPCProvider
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.views import View
from django.shortcuts import render
from accounts.models import WalletProfile
import json,sys

User = get_user_model()
class SendTransactionView(View):
    def post(self,request, *args, **kwargs):
        if request.method == 'POST':
            query = request.POST.get("value")
            value = int(query) * 100000
            # 1Blowあたり10000weiとして送金します
            print(value)
            from_wallet = WalletProfile.objects.get(user=request.user)
            to_user = request.POST.get("username")
            to_user = User.objects.get(username=to_user)
            to_wallet = WalletProfile.objects.get(user=to_user)
            """DEBUG用
            print(from_wallet.num)
            print(request.user)
            print(query)
            """
            web3 = Web3(KeepAliveRPCProvider(host='localhost', port='8545'))
            web3.personal.signAndSendTransaction(formatters.input_transaction_formatter(web3.eth, {'to': to_wallet.num, 'from': from_wallet.num, 'value': value}), request.user.username)
            return render(request, "home.html")

class SendTokenTransactionView(View):
    def post(self,request, *args, **kwargs):
        if request.method == 'POST':
            from_wallet = WalletProfile.objects.get(user=request.user)
            to_user = request.POST.get("username")
            to_user = User.objects.get(username=to_user)
            to_wallet = WalletProfile.objects.get(user=to_user)
            web3 = Web3(KeepAliveRPCProvider(host='localhost', port='8545'))
            web3.personal.unlockAccount(to_wallet.num, to_user.username)
            # 暫定的にABIを直接入力(どのトークンでも共通)
            abi=json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"success","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"success","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_value","type":"uint256"}],"name":"burn","outputs":[{"name":"success","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"standard","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_value","type":"uint256"}],"name":"burnFrom","outputs":[{"name":"success","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"},{"name":"_extraData","type":"bytes"}],"name":"approveAndCall","outputs":[{"name":"success","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"inputs":[{"name":"initialSupply","type":"uint256"},{"name":"tokenName","type":"string"},{"name":"decimalUnits","type":"uint8"},{"name":"tokenSymbol","type":"string"}],"payable":false,"type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Burn","type":"event"}]')
            cnt = web3.eth.contract(abi, "0xd32a2d87f45671afdd26be4862c8c3da91ea7b43", "My")

            print(cnt.abi)
            cnt.transact(transaction={'from': web3.eth.coinbase}).transfer(to_wallet.num, 10)
            #web3.eth.contract()
        return render(request, "home.html")
