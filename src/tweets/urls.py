from django.conf.urls import url
from .views import (
    TweetCreateView,
    TweetDetailView,
    TweetListView
    )

urlpatterns = [
    url(r'^$', TweetListView.as_view(), name='list'),
    url(r'^create/$', TweetCreateView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', TweetDetailView.as_view(), name='detail'),
]
