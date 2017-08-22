from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404

User = get_user_model()

# Create your views here.

class UserTokenView(DetailView):
    template_name = 'tokens/user_token.html'

    def get_object(self):
        user = User.objects.get(username=self.kwargs.get("username"))
        return get_object_or_404(
            User,
            username__iexact=self.kwargs.get("username")
        )