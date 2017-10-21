from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.views.generic import DetailView
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import FormView, UpdateView
from django.core.urlresolvers import reverse_lazy

from web3 import Web3, KeepAliveRPCProvider

from .forms import UserRegisterForm, UserUpdateForm, UserProfileUpdateForm
from .models import UserProfile,WalletProfile

# Create your views here.

User = get_user_model()


class UserRegisterView(FormView):
    template_name = 'accounts/user_register_form.html'
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form):
        web3 = Web3(KeepAliveRPCProvider(host='localhost', port='8545'))
        if web3.isConnected():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            new_user = User.objects.create(username=username, email=email)
            new_user.set_password(password)
            # host='localhost' port=8545 は　geth のデフォルト値
            wallet_num = web3.personal.newAccount(username)
            # geth サーバーにアクセスしてwallet発行
            wallet = WalletProfile.objects.create(user=new_user)
            # Userモデルに格納するwalletオブジェクトを生成
            new_user.wallet.num = wallet_num
            wallet.save()
            # wallet.saveでuser.wallet.numにセーブ
            new_user.save()
            return super(UserRegisterView, self).form_valid(form)
        else:
            raise PermissionDenied
            return 0


class UserDetailView(DetailView):
    template_name = 'accounts/user_detail.html'
    queryset = User.objects.all()
    slug_field = 'username'

    def __calc_balance(usr):
        web3 = Web3(KeepAliveRPCProvider(host='localhost', port='8545'))
        user = User.objects.get(username=usr.kwargs.get("username"))
        print(user.wallet) #walletidを確認する用に便利なので、少し残しておく
        user.wallet.balance = web3.eth.getBalance(user.wallet.num)/100000
        user.wallet.save()
        return 0

    def get_object(self):
        user = User.objects.get(username=self.kwargs.get("username"))
        UserDetailView.__calc_balance(self)
        return get_object_or_404(
            User,
            username__iexact=self.kwargs.get("username")
        )

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailView, self).get_context_data(*args, **kwargs)
        following = UserProfile.objects.is_following(
            self.request.user,
            self.get_object())
        context['following'] = following
        context['recommended'] = UserProfile.objects.recommended(self.request.user)
        return context

class UserFollowView(View):
    def get(self, request: object, username: object, args: object, kwargs: object) -> object:
        toggle_user = get_object_or_404(User, username__iexact=username)
        if request.user.is_authenticated():
            is_following = UserProfile.objects.toggle_follow(request.user, toggle_user)
        return redirect("profiles:detail", username=username)


# 現状使用していない
class UserUpdateView(UpdateView):
    template_name = 'accounts/user_update.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('home')

    def get_object(self):
        obj = get_object_or_404(
                User,
                username__iexact=self.kwargs.get("username")
                )
        if not obj.username == self.request.user.username:
            raise PermissionDenied
        else:
            return obj


class UserProfileUpdateView(UpdateView):
    template_name = 'accounts/user_update.html'
    form_class = UserProfileUpdateForm
    success_url = reverse_lazy('home')

    def get_object(self):
        obj = get_object_or_404(
                UserProfile,
                user=self.request.user
                )
        if not obj.user == self.request.user:
            raise PermissionDenied
        else:
            return obj
