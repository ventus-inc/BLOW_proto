from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.views.generic import DetailView
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.views.generic.edit import FormView, UpdateView
from django.core.urlresolvers import reverse_lazy

from .models import UserProfile
from .forms import UserRegisterForm, UserUpdateForm, UserProfileUpdateForm

# Create your views here.

User = get_user_model()

class UserRegisterView(FormView):
    template_name = 'accounts/user_register_form.html'
    form_class = UserRegisterForm
    success_url = '/login'

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        new_user = User.objects.create(username=username, email=email)
        new_user.set_password(password)
        new_user.save()
        return super(UserRegisterView, self).form_valid(form)

class UserDetailView(DetailView):
    template_name = 'accounts/user_detail.html'
    queryset = User.objects.all()
    slug_field = 'username'

    def get_object(self):
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
    def get(self, request, username, *args, **kwargs):
        toggle_user = get_object_or_404(User, username__iexact=username)
        if request.user.is_authenticated():
            is_following = UserProfile.objects.toggle_follow(request.user, toggle_user)
        return redirect("profiles:detail", username=username)


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
        print(self.request.user)
        print(self.kwargs.get("user"))
        obj = get_object_or_404(
                UserProfile,
                user=self.request.user
                )
        print(obj)
        print(obj.user == self.request.user)
        if not obj.user == self.request.user:
            raise PermissionDenied
        else:
            return obj
