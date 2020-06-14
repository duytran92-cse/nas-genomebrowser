
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^list$',   actions.List.as_view(),     name='treatment_block_version_list'),
    url(r'^update/(?P<text_id>([0-9]+))$', actions.Update.as_view(),   name='treatment_block_version_update'),
    url(r'^delete/(?P<text_id>([0-9]+))$', actions.Delete.as_view(),   name='treatment_block_version_delete'),
    url(r'^active/(?P<text_id>([0-9]+))$', actions.Active.as_view(),   name='treatment_block_version_active'),
]
