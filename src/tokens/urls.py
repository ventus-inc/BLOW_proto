from django.conf.urls import url

from .views import (
	UserTokenView,
    )

urlpatterns = [
    url(r'^(?P<username>[\w.@+-]+)/$', UserTokenView.as_view(), name='token'),
]
