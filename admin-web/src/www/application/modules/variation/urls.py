
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^$',                    actions.List.as_view(),     name='variation_list'),
    url(r'^list$',                    actions.List.as_view(),     name='variation_list'),
    url(r'^create$',                  actions.Create.as_view(),   name='variation_create'),
    url(r'^delete/(?P<id>([0-9]+))$', actions.Delete.as_view(),   name='variation_delete'),

    url(r'^update/(?P<variation_id>([0-9]+))$',   actions.Update.as_view(),   name='variation_update'),
    url(r'^detail/(?P<variation_id>([0-9]+))/block/',    include('application.modules.variation.block.urls')),
    url(r'^detail/(?P<variation_id>([0-9]+))/comment/',    include('application.modules.variation.comment.urls')),
    url(r'^summary/(?P<variation_id>([0-9]+))$',            actions.Summary.as_view(),   name='variation_summary'),
]
