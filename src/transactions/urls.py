from django.conf.urls import url, include

from .views import (
    SendTransactionView,
    )

urlpatterns = [
    url(r'^send_transaction/$', SendTransactionView.as_view(), name='send')
    #url(r'^(?P<username>[\w.@+-]+)/update/$', UserUpdateView.as_view(), name='update'),

]
