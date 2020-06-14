
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^list$',   actions.List.as_view(),     name='variation_block_list'),
    url(r'^create$', actions.Create.as_view(),   name='variation_block_create'),
    url(r'^update/(?P<id>([0-9]+))$', actions.Update.as_view(),   name='variation_block_update'),
    url(r'^delete/(?P<id>([0-9]+))$', actions.Delete.as_view(),   name='variation_block_delete'),

	url(r'^detail/(?P<variation_block_id>([0-9]+))/version/', include('application.modules.variation.block.version.urls')),
    url(r'^detail/(?P<variation_block_id>([0-9]+))/pub_version/', include('application.modules.variation.block.publication_version.urls')),
    url(r'^detail/(?P<variation_block_id>([0-9]+))/pub_text_version/', include('application.modules.variation.block.publication_text_version.urls')),
    url(r'^detail/(?P<variation_block_id>([0-9]+))/disgenet_diseases_version/', include('application.modules.variation.block.disgenet_diseases_version.urls')),
    url(r'^detail/(?P<variation_block_id>([0-9]+))/eff_version/', include('application.modules.variation.block.effect_version.urls')),
    url(r'^detail/(?P<variation_block_id>([0-9]+))/fre_version/', include('application.modules.variation.block.frequency_version.urls')),
    url(r'^detail/(?P<variation_block_id>([0-9]+))/alias_version/', include('application.modules.variation.block.alias_version.urls')),
    url(r'^detail/(?P<variation_block_id>([0-9]+))/infobox_version/', include('application.modules.variation.block.infobox_version.urls')),
]
