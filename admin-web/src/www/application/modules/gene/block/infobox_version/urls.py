
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^list$',   actions.List.as_view(),     name='gene_block_infobox_version_list'),
    url(r'^update/(?P<infobox_id>([0-9]+))$', actions.Update.as_view(),   name='gene_block_infobox_version_update'),
    url(r'^delete/(?P<infobox_id>([0-9]+))$', actions.Delete.as_view(),   name='gene_block_infobox_version_delete'),
    url(r'^active/(?P<text_id>([0-9]+))$', actions.Active.as_view(),   name='gene_block_infobox_version_active'),
    url(r'^active_sum/(?P<text_id>([0-9]+))$', actions.ActiveSum.as_view(),   name='gene_block_infobox_version_active_sum'),
]
