from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import (
    DetailView)
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist

from web3 import Web3, HTTPProvider, KeepAliveRPCProvider

from .models import Token, BuyOrder, SellOrder, TokenBoard
from accounts.models import WalletProfile, UserProfile

import sys, json
from time import sleep

User = get_user_model()


# Create your views here.

class BuyUserTokenView(DetailView):
    template_name = 'tokens/buy_user_tokens.html'

    def get_context_data(self, **kwargs):
        context = super(BuyUserTokenView, self).get_context_data(**kwargs)
        user = User.objects.get(username=self.kwargs.get("username"))
        context['sells'] = SellOrder.objects.get_summed_lot(user)
        context['buys'] = BuyOrder.objects.get_summed_lot(user)
        context['buy_lists'] = BuyOrder.objects.get_summed_list(user)
        context['sell_lists'] = SellOrder.objects.get_summed_list(user)
        return context

    def get_object(self):
        # user = User.objects.get(username=self.kwargs.get("username"))
        return get_object_or_404(
            User,
            username__iexact=self.kwargs.get("username")
        )


class SellUserTokenView(DetailView):
    template_name = 'tokens/sell_user_tokens.html'

    def get_context_data(self, **kwargs):
        context = super(SellUserTokenView, self).get_context_data(**kwargs)
        user = User.objects.get(username=self.kwargs.get("username"))
        context['sells'] = SellOrder.objects.get_summed_lot(user)
        context['buys'] = BuyOrder.objects.get_summed_lot(user)
        context['buy_lists'] = BuyOrder.objects.get_summed_list(user)
        context['sell_lists'] = SellOrder.objects.get_summed_list(user)
        TokenBoard.object.get_seller(user)
        return context

    def get_object(self):
        # user = User.objects.get(username=self.kwargs.get("username"))
        return get_object_or_404(
            User,
            username__iexact=self.kwargs.get("username")
        )


# TODO: BuyTokenView, BuyTokenConfirmView をformsで書き換え
class BuyTokenView(LoginRequiredMixin, View):
    """Token購入するView。売買板の表示と、BuyTokenConfirmViewへの遷移をする
    """

    def post(self, request, *args, **kwargs):
        if request.method == 'POST' and request.user.is_authenticated():
            master = User.objects.get(username=self.kwargs.get("username"))
            lot = request.POST.get("lot")
            price = request.POST.get("value")
            # TODO: formでバリデーションとる&変数型変換
            if int(lot) <= 0 or float(price) <= 0:
                return HttpResponse("Invalid input")
            context = {
                'master': master,
                'buyer': request.user,
                'price': price,
                'lot': lot,
            }
            return render(request, "tokens/buy_confirm.html", context=context)


# TODO: SellTokenView, SellTokenConfirmView をformsで書き換え
class SellTokenView(LoginRequiredMixin, View):
    """Token購入するView。売買板の表示と、SellTokenConfirmViewへの遷移をする
    """

    def post(self, request, *args, **kwargs):
        if request.method == 'POST' and request.user.is_authenticated():
            master = User.objects.get(username=self.kwargs.get("username"))
            lot = request.POST.get("lot")
            price = request.POST.get("value")
            # TODO: formでバリデーションとる&変数型変換
            if int(lot) <= 0 or float(price) <= 0:
                return HttpResponse("Invalid input")
            context = {
                'master': master,
                'seller': request.user,
                'price': price,
                'lot': lot,
            }
            return render(request, "tokens/sell_confirm.html", context=context)


class BuyTokenConfirmView(LoginRequiredMixin, View):
    """Token購入の確認をするView
    """

    def post(self, request, *args, **kwargs):
        if request.method == 'POST' and request.user.is_authenticated():
            master = User.objects.get(username=self.kwargs.get("username"))
            lot = request.POST.get("lot")
            price = request.POST.get("value")
            # TODO: formでバリデーションとる&変数型変換
            if int(lot) <= 0 or float(price) <= 0:
                return HttpResponse("Invalid input")
            buyer = User.objects.get(username=request.user.username)
            password = request.POST.get("password")
            success = buyer.check_password(password)
            # TODO: formでvalidation取るようにする
            if success:
                obj = BuyOrder(
                    master=master,
                    buyer=request.user,
                    price=price,
                    lot=lot,
                )
                obj.save()
                try:

                    exist = SellOrder.objects.filter(
                        price__icontains=price, master=master).first()
                except SellOrder.DoesNotExist:
                    exist = None
                # if SellOrder.objects.get(price__iexact=price) is not None:

                if exist is not None:
                    seller = SellOrder.objects.filter(master=master, price=price)[0].seller
                    if int(lot) <= SellOrder.objects.filter(master=master, price=price)[0].lot:
                        seller.wallet.selling_token -= int(lot)
                        seller.wallet.save()
                    else:
                        seller.wallet.selling_token = SellOrder.objects.filter(master=master, price=price)[0].lot
                    send_token_transaction(buyer,
                                           int(obj.lot),
                                           master.profile.token_address,
                                           False,
                                           seller,)
                    token_transaction_check(SellOrder.objects.filter(master=master, price=price)[0],
                                            BuyOrder.objects.filter(master=master, buyer=buyer, price=price)[0])

                    print(seller.wallet.selling_token)

                    buyer.save()
                return redirect("home")

            else:
                return HttpResponse("Password Incorrect")


class SellTokenConfirmView(LoginRequiredMixin, View):
    """Token購入の確認をするView
    """

    def post(self, request, *args, **kwargs):
        if request.method == 'POST' and request.user.is_authenticated():
            master = User.objects.get(username=self.kwargs.get("username"))
            lot = request.POST.get("lot")
            price = request.POST.get("value")
            # TODO: formでバリデーションとる&変数型変換
            if int(lot) <= 0 or float(price) <= 0:
                return HttpResponse("Invalid input")

            seller = User.objects.get(username=request.user.username)
            seller_wallet = seller.wallet
            # TODO 各自のユーザーのアドレスへ
            print(seller.profile.token_address)
            token_address = master.profile.token_address
            print(token_address)
            seller_lot = seller.wallet.get_token_lot(token_address)
            selling_token = seller.wallet.selling_token
            if (seller_lot - selling_token) < int(lot):
                return HttpResponse("token足りない")
            password = request.POST.get("password")
            success = seller.check_password(password)
            # TODO: formでvalidation取るようにする
            if success:
                obj = SellOrder(
                    master=master,
                    seller=request.user,
                    price=price,
                    lot=lot,
                )

                obj.save()
                try:

                    exist = BuyOrder.objects.filter(
                        price__icontains=price, master=master).first()

                except BuyOrder.DoesNotExist:
                    exist = None
                if exist is not None:
                    buyer = BuyOrder.objects.filter(master=master, price=price)[0].buyer
                    token_transaction_check(BuyOrder.objects.filter(master=master,
                                                                    price=price)[0],
                                            SellOrder.objects.filter(master=master,
                                                                     seller=seller,
                                                                     price=price)[0])
                    send_token_transaction(buyer,
                                           int(obj.lot),
                                           token_address,
                                           False,
                                           seller)
                else:
                    seller.wallet.selling_token += int(obj.lot)
                    seller.wallet.save()

                print(seller.wallet.selling_token)
                return redirect("home")
            else:
                return HttpResponse("Password Incorrect")


class MyAssetTokensView(LoginRequiredMixin, DetailView):
    """保持しているTokenの情報を表示するページ
    """
    template_name = 'tokens/asset_token.html'

    def get_object(self):
        # user = User.objects.get(username=self.kwargs.get("username"))
        return get_object_or_404(
            User,
            username__iexact=self.kwargs.get("username")
        )

    def get_context_data(self, *args, **kwargs):
        context = super(MyAssetTokensView, self).get_context_data(
            *args, **kwargs)
        requested_user = User.objects.get(username=self.kwargs.get("username"))
        requesting_user = self.request.user
        if not requested_user == requesting_user:
            raise PermissionDenied
        token = Token.objects.filter(buyer=requested_user)
        context['user'] = requested_user
        context['tokens'] = token
        return context


class TokenIssueView(View):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST' and request.user.is_authenticated():
            to_user = User.objects.get(username=request.user.username)
            to_wallet = WalletProfile.objects.get(user=to_user)
            token_dir = '../contract/Token/FixedSupplyToken'
            # Tokenの発行量
            issue_lot = 1000000
            web3 = Web3(KeepAliveRPCProvider(host='localhost', port='8545'))
            token_binary = token_dir + '.bin'
            token_abi = token_dir + '.abi'
            binary = open(token_binary)
            abi = open(token_abi)
            abi = json.loads(abi.read())
            cnt = web3.eth.contract()
            cnt.bytecode = '0x' + binary.read()
            cnt.abi = abi

            # TODO トークン発行時のパスフレーズを入力できるようにする
            admin = UserProfile.objects.first()
            unlock_validation(web3.eth.coinbase,admin.user.username,web3)
            #web3.personal.unlockAccount(web3.eth.coinbase, admin.user.username)
            # print(admin.user.password)
            transaction_hash = cnt.deploy(transaction={'from': web3.eth.coinbase, 'gas': 1000000})
            sleep(4)
            hash_detail = web3.eth.getTransactionReceipt(transaction_hash)
            #DEBUG print(hash_detail.contractAddress)
            token_address = hash_detail.contractAddress
            token_user = User.objects.get(username=request.user.username)
            token_user.profile.token_address = token_address
            token_user.profile.save()

            from_wallet = WalletProfile.objects.filter(num=web3.eth.coinbase).first()
            send_token_transaction(to_user, issue_lot, token_address, True, from_wallet.user)
            return redirect("home")


def token_transaction_check(now_user, previous_user):
    if now_user.lot >= previous_user.lot:
        token_transaction_confirm(now_user, previous_user)
    else:
        token_transaction_confirm(previous_user, now_user)
    return 0


def token_transaction_confirm(higher, lower):
    higher.lot = higher.lot - lower.lot
    higher.save()
    lower.delete()
    if higher.lot is 0:
        higher.delete()
    return 0


"""関数は作ったけど使ってない・・・


def token_board_check(BuyOrder, SellOrder):
    try:
        exist = BuyOrder.objects.filter(
            price__icontains=price, master=master).first()
    except BuyOrder.DoesNotExist:
        exist = None

    if exist is not None:
        token_transaction_check(BuyOrder.objects.filter(master=master, price=price)[0],
                                SellOrder.objects.filter(master=master, seller=seller, price=price)[0])
"""


def send_token_transaction(buyer, lot, token_address, is_issue, *seller):

    seller = seller[0]
    web3 = Web3(KeepAliveRPCProvider(host='localhost', port='8545'))
    unlock_validation(seller.wallet.num, seller.username, web3)

    f = open("transactions/abi.json", 'r')
    abi = json.loads(f.read())
    # contractのアドレスはトークンごと abiは共通
    cnt = web3.eth.contract(abi, token_address)
    # print(seller)
    # print(seller.wallet.num)
    cnt.transact(transaction={'from': seller.wallet.num}).transfer(buyer.wallet.num, lot)
    buyer.wallet.token_balance = buyer.wallet.get_token_lot(token_address)
    if is_issue is True:
        buyer.profile.have_token.add(buyer)
    else:
        print("---------------")
        buyer.profile.have_token.add(seller)
        print(token_address)
    buyer.profile.save()
    print(buyer.have_token.all())
    buyer.wallet.save()


def unlock_validation(wallet_num, passphrase, web3):
    if web3.personal.unlockAccount(wallet_num, passphrase):
        return True
    else:
        return redirect("error.html")
