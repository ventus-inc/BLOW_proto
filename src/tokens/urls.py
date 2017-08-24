from django.conf.urls import url

from .views import (
	UserTokenView,
	BuyTokenView,
    )

urlpatterns = [
    url(r'^(?P<username>[\w.@+-]+)/$', UserTokenView.as_view(), name='token'),
    # url(r'^(?P<username>[\w.@+-]+)/buy/$', BuyTokenView.as_view(), name='buy'),
    url(r'^buy/$', BuyTokenView.as_view(), name='buy')
]
