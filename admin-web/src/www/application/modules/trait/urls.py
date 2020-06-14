
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^$',                    actions.List.as_view(),     name='trait_list'),
    url(r'^list$',                    actions.List.as_view(),     name='trait_list'),
    url(r'^create$',                  actions.Create.as_view(),   name='trait_create'),
    url(r'^delete/(?P<id>([0-9]+))$', actions.Delete.as_view(),   name='trait_delete'),

    url(r'^update/(?P<trait_id>([0-9]+))$',   actions.Update.as_view(),   name='trait_update'),
    url(r'^detail/(?P<trait_id>([0-9]+))/block/',    include('application.modules.trait.block.urls')),
    url(r'^detail/(?P<trait_id>([0-9]+))/comment/',    include('application.modules.trait.comment.urls')),
    url(r'^summary/(?P<trait_id>([0-9]+))$',   actions.Summary.as_view(),   name='trait_summary'),
]
