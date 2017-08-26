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
    	context['buys'] = BuyOrder.objects.filter(master=user).order_by('-price')
    	print(context['user'])
    	print(context['buys'])
    	total_buys = []
    	previous_price = None
    	obj = BuyOrder()
    	for i in context['buys']:
    		if not previous_price:
    			obj = BuyOrder(
					master = i.master,
					buyer = i.buyer,
					price = i.price,
					lot = i.lot,
    				)
    		if not previous_price == i.price and previous_price:
    			total_buys.append(obj)
    			obj = BuyOrder(
					master = i.master,
					buyer = i.buyer,
					price = i.price,
					lot = i.lot,
    				)
    		else:
    			obj.lot += i.lot
    			# total_buys.append(obj)
    		print(i.buyer)
    		print(i.price)
    		print(i.lot)
    		print(len(context['buys']))
    		previous_price = i.price
    	total_buys.append(obj)
    	context['total_buys'] = total_buys
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
			master = User.objects.get(username=self.kwargs.get("username"))
			lot = request.POST.get("lot")
			price = request.POST.get("value")
			obj = BuyOrder(
				master = master,
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
