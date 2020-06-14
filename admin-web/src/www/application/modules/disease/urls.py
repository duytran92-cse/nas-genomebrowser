
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^$',                    actions.List.as_view(),     name='disease_list'),
    url(r'^list$',                    actions.List.as_view(),     name='disease_list'),
    url(r'^create$',                  actions.Create.as_view(),   name='disease_create'),
    url(r'^delete/(?P<id>([0-9]+))$', actions.Delete.as_view(),   name='disease_delete'),

    url(r'^update/(?P<disease_id>([0-9]+))$',   actions.Update.as_view(),   name='disease_update'),
    url(r'^detail/(?P<disease_id>([0-9]+))/block/',    include('application.modules.disease.block.urls')),
    url(r'^detail/(?P<disease_id>([0-9]+))/comment/',    include('application.modules.disease.comment.urls')),
    url(r'^summary/(?P<disease_id>([0-9]+))$',   actions.Summary.as_view(),   name='disease_summary'),
]
