from django.views.generic.edit import FormView
from web3 import Web3,formatters,KeepAliveRPCProvider
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.views import View
from django.shortcuts import render
from accounts.models import WalletProfile

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
            query = request.POST.get("value")
            value = int(query) * 100000
            # 1Blowあたり10000weiとして送金します
            print(value)
            from_wallet = WalletProfile.objects.get(user=request.user)
            to_user = request.POST.get("username")
            to_user = User.objects.get(username=to_user)
            to_wallet = WalletProfile.objects.get(user=to_user)
            web3 = Web3(KeepAliveRPCProvider(host='localhost', port='8545'))
        return render(request, "home.html")