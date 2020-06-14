
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^$',      actions.Search.as_view(),      name='search')
]
