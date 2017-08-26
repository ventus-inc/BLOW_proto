from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views import View
from django.views.generic import (
	DetailView)
from django.shortcuts import get_object_or_404, redirect
from datetime import datetime

from .models import BuyOrder

User = get_user_model()

# Create your views here.

class UserTokenView(DetailView):
    template_name = 'tokens/user_token.html'

    def get_context_data(self, **kwargs):
    	context = super(UserTokenView, self).get_context_data(**kwargs)
    	user = User.objects.get(username=self.kwargs.get("username"))
    	context['user'] = user
    	context['buys'] = BuyOrder.objects.filter(master=user)
    	print(context['user'])
    	print(context['buys'])
    	return context

    def get_object(self):
        user = User.objects.get(username=self.kwargs.get("username"))
        return get_object_or_404(
            User,
            username__iexact=self.kwargs.get("username")
        )

class BuyTokenView(LoginRequiredMixin, View):
	def post(self, request, *args, **kwargs):
		if request.method == 'POST' and request.user.is_authenticated():
			lot = request.POST.get("lot")
			price = request.POST.get("value")
			obj = BuyOrder(
				buyer = request.user,
				price = price,
				lot = lot,
				)
			obj.save()
			print(request.user)
			print(lot)
			print(price)
			# return render(request, "home.html")
			return redirect("home")

	def get_object(self):
		user = User.objects.get(username=self.kwargs.get("username"))
		return get_object_or_404(
		    User,
		    username__iexact=self.kwargs.get("username")
		)
