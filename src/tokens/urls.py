from django.conf.urls import url
from .views import (
	BuyUserTokenView,
    SellUserTokenView,
	BuyTokenView,
    SellTokenView,
	BuyTokenConfirmView,
    SellTokenConfirmView,
	MyAssetTokensView,
    TokenIssueView,
    )

urlpatterns = [
    url(r'^(?P<username>[\w.@+-]+)/buy_token$', BuyUserTokenView.as_view(), name='buy_token'),
    url(r'^(?P<username>[\w.@+-]+)/sell_token$', SellUserTokenView.as_view(), name='sell_token'),
    url(r'^(?P<username>[\w.@+-]+)/buy/$', BuyTokenView.as_view(), name='buy'),
    url(r'^(?P<username>[\w.@+-]+)/sell/$', SellTokenView.as_view(), name='sell'),
    url(r'^(?P<username>[\w.@+-]+)/buy/confirm$', BuyTokenConfirmView.as_view(), name='buy_confirm'),
    url(r'^(?P<username>[\w.@+-]+)/sell/confirm$', SellTokenConfirmView.as_view(), name='sell_confirm'),
    url(r'^(?P<username>[\w.@+-]+)/asset$', MyAssetTokensView.as_view(), name='asset'),
    url(r'^issue/$', TokenIssueView.as_view(), name='issue'),
    # url(r'^buy/$', BuyTokenView.as_view(), name='buy')
]
