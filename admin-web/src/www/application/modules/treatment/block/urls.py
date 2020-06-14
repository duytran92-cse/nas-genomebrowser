
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^list$',   actions.List.as_view(),     name='treatment_block_list'),
    url(r'^create$', actions.Create.as_view(),   name='treatment_block_create'),
    url(r'^update/(?P<id>([0-9]+))$', actions.Update.as_view(),   name='treatment_block_update'),
    url(r'^delete/(?P<id>([0-9]+))$', actions.Delete.as_view(),   name='treatment_block_delete'),

	url(r'^detail/(?P<treatment_block_id>([0-9]+))/version/', include('application.modules.treatment.block.version.urls')),
    url(r'^detail/(?P<treatment_block_id>([0-9]+))/pub_version/', include('application.modules.treatment.block.publication_version.urls')),
    url(r'^detail/(?P<treatment_block_id>([0-9]+))/alias_version/', include('application.modules.treatment.block.alias_version.urls')),
]
