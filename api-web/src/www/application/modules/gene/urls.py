
from django.conf.urls import include, url
from . import handlers

urlpatterns = [
    url(r'^get$',    handlers.Get.as_view(),      name='gene_get'),
    url(r'^view$',    handlers.View.as_view(),      name='gene_view'),
    url(r'^list$',   handlers.List.as_view(),     name='gene_list'),
    url(r'^create$',    handlers.Create.as_view(),      name='gene_create'),
    url(r'^update$',   handlers.Update.as_view(),     name='gene_update'),
    url(r'^delete$',    handlers.Delete.as_view(),      name='gene_delete'),
    url(r'^summary$',    handlers.Summary.as_view(),      name='gene_summary')
]
