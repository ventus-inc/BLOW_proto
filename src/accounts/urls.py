from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from .views import (
    UserDetailView,
    UserFollowView,
    UserUpdateView,
    UserProfileUpdateView,
    )

urlpatterns = [
    # url(r'^$', RedirectView.as_view(url="/")),
    # url(r'^$', TweetListAPIView.as_view(), name='list'), # /api/tweet/
    # url(r'^create/$', TweetCreateAPIView.as_view(), name='create'), # /api/tweet/
    # url(r'^create/$', TweetCreateView.as_view(), name='create'),
    url(r'^(?P<username>[\w.@+-]+)/$', UserDetailView.as_view(), name='detail'),
    url(r'^(?P<username>[\w.@+-]+)/follow/$', UserFollowView.as_view(), name='follow'),
    # 現状使用していない
    url(r'^(?P<username>[\w.@+-]+)/update/$', UserUpdateView.as_view(), name='update'),
    url(r'^(?P<username>[\w.@+-]+)/update_profile/$', UserProfileUpdateView.as_view(), name='update_profile'),
    # url(r'^(?P<pk>\d+)/delete/$', TweetDeleteView.as_view(), name='delete')
]
