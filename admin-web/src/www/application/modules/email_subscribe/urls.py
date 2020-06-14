
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^$',                        actions.List.as_view(),     name='email_subscribe_list'),
    url(r'^list$',                    actions.List.as_view(),     name='email_subscribe_list'),
    url(r'^create$',                  actions.Create.as_view(),   name='email_subscribe_create'),
    url(r'^delete/(?P<id>([0-9]+))$', actions.Delete.as_view(),   name='email_subscribe_delete'),
    url(r'^update/(?P<id>([0-9]+))$',   actions.Update.as_view(),   name='email_subscribe_update'),

]
