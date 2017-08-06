from django.contrib.auth import get_user_model
from django.views.generic import DetailView
from django.shortcuts import render

# Create your views here.

User = get_user_model()

class UserDetailView(DetailView):
    template_name = 'accounts/user_detail.html'
    queryset = User.objects.all()
