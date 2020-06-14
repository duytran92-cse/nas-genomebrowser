
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^$',                    actions.List.as_view(),     name='gene_list'),
    url(r'^list$',                    actions.List.as_view(),     name='gene_list'),
    url(r'^create$',                  actions.Create.as_view(),   name='gene_create'),
    url(r'^delete/(?P<id>([0-9]+))$', actions.Delete.as_view(),   name='gene_delete'),

    url(r'^update/(?P<gene_id>([0-9]+))$',   actions.Update.as_view(),   name='gene_update'),
    url(r'^detail/(?P<gene_id>([0-9]+))/block/',    include('application.modules.gene.block.urls')),
    url(r'^detail/(?P<gene_id>([0-9]+))/comment/',    include('application.modules.gene.comment.urls')),
    url(r'^summary/(?P<gene_id>([0-9]+))$',   actions.Summary.as_view(),   name='gene_summary'),
]
