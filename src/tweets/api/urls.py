from django.conf.urls import url
from django.views.generic.base import RedirectView
from .views import (
    LikeToggleAPIView,
    RetweetAPIView,
    TweetListAPIView,
    TweetCreateAPIView,
    TweetDetailAPIView,
    TweetDeleteAPIView,
    )

urlpatterns = [
    # url(r'^$', RedirectView.as_view(url="/")),
    url(r'^$', TweetListAPIView.as_view(), name='list'), # /api/tweet/
    url(r'^create/$', TweetCreateAPIView.as_view(), name='create'), # /api/tweet/
    url(r'^(?P<pk>\d+)/$', TweetDetailAPIView.as_view(), name='detail'), # /api/tweet/
    # url(r'^create/$', TweetCreateView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/retweet$', RetweetAPIView.as_view(), name='retweet'),
    url(r'^(?P<pk>\d+)/like/$', LikeToggleAPIView.as_view(), name='like'),
    url(r'^(?P<pk>\d+)/delete/$', TweetDeleteAPIView.as_view(), name='delete'),
    # url(r'^(?P<pk>\d+)/update/$', TweetUpdateView.as_view(), name='update'),
    # url(r'^(?P<pk>\d+)/delete/$', TweetDeleteView.as_view(), name='delete')
]
