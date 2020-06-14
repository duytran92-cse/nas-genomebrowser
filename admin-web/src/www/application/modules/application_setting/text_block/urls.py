
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^list$',                                      actions.List.as_view(),     name='text_block_list'),
    url(r'^create$',                                    actions.Create.as_view(),   name='text_block_create'),
    url(r'^delete/(?P<id>([0-9]+))$',                   actions.Delete.as_view(),   name='text_block_delete'),
    url(r'^update/(?P<text_block_id>([0-9]+))$',        actions.Update.as_view(),   name='text_block_update')
]
