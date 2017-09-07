from django.conf.urls import url

from .views import (
    SendTransactionView,
    SendTokenTransactionView,
    )

urlpatterns = [
url(r'^send_transaction/$', SendTransactionView.as_view(), name='send'),
url(r'^send_token_transaction/$', SendTokenTransactionView.as_view(), name='sendtoken')
]
