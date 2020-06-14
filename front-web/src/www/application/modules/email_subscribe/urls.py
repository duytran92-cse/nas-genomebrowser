
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^create$',          actions.EmailSubcibe.as_view(),      name='email_subscribe_create'),
    url(r'^$',                actions.EmailSubcibe.as_view(),      name='email_subscribe_create'),

]
