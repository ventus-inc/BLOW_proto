from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import (
	DetailView)
from django.shortcuts import get_object_or_404, redirect
from datetime import datetime

from .models import Token, BuyOrder

User = get_user_model()

# Create your views here.

class UserTokenView(DetailView):
    template_name = 'tokens/user_token.html'

    def get_context_data(self, **kwargs):
    	context = super(UserTokenView, self).get_context_data(**kwargs)
    	user = User.objects.get(username=self.kwargs.get("username"))
    	context['buys'] = BuyOrder.objects.get_summed_lot(user)
    	return context

    def get_object(self):
        user = User.objects.get(username=self.kwargs.get("username"))
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
			if int(lot) < 0 or float(price) < 0:
				return HttpResponse("Invalid input")
			context = {
				'master': master,
				'buyer': request.user,
				'price': price,
				'lot': lot,
			}
			return render(request, "tokens/buy_confirm.html", context=context)


class BuyTokenConfirmView(LoginRequiredMixin, View):
	"""Token購入の確認をするView
	"""
	def post(self, request, *args, **kwargs):
		if request.method == 'POST' and request.user.is_authenticated():
			master = User.objects.get(username=self.kwargs.get("username"))
			lot = request.POST.get("lot")
			price = request.POST.get("value")
			# TODO: formでバリデーションとる&変数型変換
			if int(lot) < 0 or float(price) < 0:
				return HttpResponse("Invalid input")
			buyer = User.objects.get(username=request.user.username)
			password = request.POST.get("password")
			success = buyer.check_password(password)
			# TODO: formでvalidation取るようにする
			if success:
				obj = BuyOrder(
					master = master,
					buyer = request.user,
					price = price,
					lot = lot,
					)
				obj.save()
				return redirect("home")
			else:
				return HttpResponse("Password Incorrect")

class MyAssetTokensView(LoginRequiredMixin, DetailView):
	"""保持しているTokenの情報を表示するページ
	"""
	template_name = 'tokens/asset_token.html'
	def get_object(self):
		user = User.objects.get(username=self.kwargs.get("username"))
		return get_object_or_404(
			User,
			username__iexact=self.kwargs.get("username")
		)

	def get_context_data(self, *args, **kwargs):
		context = super(MyAssetTokensView, self).get_context_data(*args, **kwargs)
		requested_user = User.objects.get(username=self.kwargs.get("username"))
		requesting_user = self.request.user
		if not requested_user == requesting_user:
			raise PermissionDenied
		token = Token.objects.filter(buyer=requested_user)
		context['user'] = requested_user
		context['tokens'] = token
		return context

