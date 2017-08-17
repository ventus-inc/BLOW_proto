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
            wallet = WalletProfile.objects.get(user=request.user)
            print(wallet.num)
            print(request.user)
            print(query)
            web3 = Web3(KeepAliveRPCProvider(host='localhost', port='8545'))
            web3.personal.signAndSendTransaction(formatters.input_transaction_formatter(web3.eth, {'to': '0x458e7a9411dd0fea48fdccea2772a074677d4d2b', 'from': wallet.num, 'value': query}), 'aaa')
            return render(request, "home.html")







class SearchView(View):
    def get(self, request, *args, **kwargs):
        # query = User.objects.all()
        query = request.GET.get("q")
        qs = None
        if query:
            qs = User.objects.filter(
                    Q(username__icontains=query)
                )
        context = {"users": qs}
        return render(request, "search.html", context)
