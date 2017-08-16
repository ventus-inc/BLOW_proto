from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.views.generic import DetailView
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView, UpdateView
from django.core.urlresolvers import reverse_lazy

from .models import UserProfile
from .forms import UserRegisterForm

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


# class UserUpdateView(UpdateView):
#     template_name = 'accounts/user_update.html'
#     queryset = User.objects.all()
#     slug_field = 'username'
#     form_class = UserUpdateForm
#     success_url = reverse_lazy('profiles:detail')

#     def get_object(self):
#         return get_object_or_404(
#             User,
#             username__iexact=self.kwargs.get("username")
#             )

#     def form_valid(self, form):
#         username = form.cleaned_data.get("username")
#         email = form.cleaned_data.get("email")
#         password = form.cleaned_data.get("password")
#         new_user = User.objects.create(username=username, email=email)
#         new_user.set_password(password)
#         new_user.save()
#         return super(UserRegisterView, self).form_valid(form)

class UserUpdateView(UpdateView):
    template_name = 'accounts/user_update.html'
    model = User
    slug_field = 'username'
    fields = ['first_name',
              'last_name',
              'email',
              ]
    success_url = reverse_lazy('home')

    def get_object(self):
        return get_object_or_404(
            User,
            username__iexact=self.kwargs.get("username")
            )

    # def form_valid(self, form):
    #     print(self.model)
    #     print(self.model.username)
    #     print(self.model.first_name)
    #     print("+++++++")
    #     print(self.object.first_name)
    #     print(self.object.last_name)
    #     print("+++++++")
    #     print()
    #     username = form.cleaned_data.get("username")
    #     email = form.cleaned_data.get("email")
    #     password = form.cleaned_data.get("password")


    #     new_user = User.objects.create(username=username, email=email)
    #     new_user.set_password(password)
    #     new_user.save()
    #     return super(UserUpdateView, self).form_valid(form)

# def user_update(request, username):
#     if request.method == 'POST':
#         form = UserChangeForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect("profiles:detail", username=username)
#         else:
#             form = UserChangeForm(instance=request.user)
#             args = {'form':form}
#             return render(request, 'accounts/user_update.html', args)
