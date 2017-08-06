from django.conf.urls import url
from django.views.generic.base import RedirectView
from .views import (
    UserDetailView,
    UserFollowView,
    )

urlpatterns = [
    # url(r'^$', RedirectView.as_view(url="/")),
    # url(r'^$', TweetListAPIView.as_view(), name='list'), # /api/tweet/
    # url(r'^create/$', TweetCreateAPIView.as_view(), name='create'), # /api/tweet/
    # url(r'^create/$', TweetCreateView.as_view(), name='create'),
    url(r'^(?P<username>[\w.@+-]+)/$', UserDetailView.as_view(), name='detail'),
    url(r'^(?P<username>[\w.@+-]+)/follow/$', UserFollowView.as_view(), name='follow'),
    # url(r'^(?P<pk>\d+)/update/$', TweetUpdateView.as_view(), name='update'),
    # url(r'^(?P<pk>\d+)/delete/$', TweetDeleteView.as_view(), name='delete')
]
