
from django.conf.urls import include, url
from . import handlers

urlpatterns = [
    url(r'^get$',    handlers.Get.as_view(),      name='gene_block_infobox_version_get'),
    url(r'^list$',   handlers.List.as_view(),     name='gene_block_infobox_version_list'),
    url(r'^update$', handlers.Update.as_view(),   name='gene_block_infobox_version_update'),
    url(r'^active$', handlers.Active.as_view(),   name='gene_block_infobox_version_active'),
]
