
from django.conf.urls import include, url
from . import handlers

urlpatterns = [
    url(r'^get$',    handlers.Get.as_view(),      name='gene_block_eff_version_get'),
    url(r'^list$',   handlers.List.as_view(),     name='gene_block_eff_version_list'),
    url(r'^update$', handlers.Update.as_view(),   name='gene_block_eff_version_update'),
    url(r'^delete$', handlers.Delete.as_view(),   name='gene_block_eff_version_delete'),
    url(r'^active$', handlers.Active.as_view(),   name='gene_block_eff_version_active'),
]
