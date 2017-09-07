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

from .models import Token, BuyOrder, SellOrder

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
<<<<<<< HEAD
        """
== == == =
    """
>>>>>>> develop

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
<< << << < HEAD
        """
=======
    """
>>>>>> > develop

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
<<<<<<< HEAD
        """
== == == =
    """
>>>>>>> develop

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
                    token_transaction_check(SellOrder.objects.filter(master=master, price=price)[0],
                                            BuyOrder.objects.filter(master=master, buyer=buyer, price=price)[0])
                return redirect("home")

            else:
                return HttpResponse("Password Incorrect")


class SellTokenConfirmView(LoginRequiredMixin, View):
    """Token購入の確認をするView
<< << << < HEAD
        """
=======
    """
>>>>>> > develop

    def post(self, request, *args, **kwargs):
        if request.method == 'POST' and request.user.is_authenticated():
            master = User.objects.get(username=self.kwargs.get("username"))
            lot = request.POST.get("lot")
            price = request.POST.get("value")
            # TODO: formでバリデーションとる&変数型変換
            if int(lot) <= 0 or float(price) <= 0:
                return HttpResponse("Invalid input")
            seller = User.objects.get(username=request.user.username)
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
                    token_transaction_check(BuyOrder.objects.filter(master=master, price=price)[0],
                                            SellOrder.objects.filter(master=master, seller=seller, price=price)[0])
                return redirect("home")
            else:
                return HttpResponse("Password Incorrect")


class MyAssetTokensView(LoginRequiredMixin, DetailView):
    """保持しているTokenの情報を表示するページ
<<<<<<< HEAD
        """
== == == =
    """
>>>>>>> develop
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
