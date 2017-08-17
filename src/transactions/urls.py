from django.conf.urls import url

from .views import (
    SendTransactionView,
    )

urlpatterns = [
    url(r'^send_transaction/$', SendTransactionView.as_view(), name='send')
]
