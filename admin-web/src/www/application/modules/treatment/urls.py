
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^$',                    actions.List.as_view(),     name='treatment_list'),
    url(r'^list$',                    actions.List.as_view(),     name='treatment_list'),
    url(r'^create$',                  actions.Create.as_view(),   name='treatment_create'),
    url(r'^delete/(?P<id>([0-9]+))$', actions.Delete.as_view(),   name='treatment_delete'),

    url(r'^update/(?P<treatment_id>([0-9]+))$',   actions.Update.as_view(),   name='treatment_update'),
    url(r'^detail/(?P<treatment_id>([0-9]+))/block/',    include('application.modules.treatment.block.urls')),
    url(r'^detail/(?P<treatment_id>([0-9]+))/comment/',    include('application.modules.treatment.comment.urls')),
    url(r'^summary/(?P<treatment_id>([0-9]+))$',   actions.Summary.as_view(),   name='treatment_summary'),
]
