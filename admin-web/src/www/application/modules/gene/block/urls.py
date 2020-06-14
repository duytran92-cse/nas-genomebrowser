
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^list$',   actions.List.as_view(),     name='gene_block_list'),
    url(r'^create$', actions.Create.as_view(),   name='gene_block_create'),
    url(r'^update/(?P<id>([0-9]+))$', actions.Update.as_view(),   name='gene_block_update'),
    url(r'^delete/(?P<id>([0-9]+))$', actions.Delete.as_view(),   name='gene_block_delete'),

	url(r'^detail/(?P<gene_block_id>([0-9]+))/version/', include('application.modules.gene.block.version.urls')),
    url(r'^detail/(?P<gene_block_id>([0-9]+))/pub_version/', include('application.modules.gene.block.publication_version.urls')),
    url(r'^detail/(?P<gene_block_id>([0-9]+))/eff_version/', include('application.modules.gene.block.effect_version.urls')),
    url(r'^detail/(?P<gene_block_id>([0-9]+))/alias_version/', include('application.modules.gene.block.alias_version.urls')),
    url(r'^detail/(?P<gene_block_id>([0-9]+))/infobox_version/', include('application.modules.gene.block.infobox_version.urls')),
]
