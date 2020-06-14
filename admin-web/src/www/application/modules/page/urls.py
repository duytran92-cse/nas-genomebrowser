
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^$',                    actions.List.as_view(),     name='page_list'),
    url(r'^list$',                    actions.List.as_view(),     name='page_list'),
    url(r'^create$',                  actions.Create.as_view(),   name='page_create'),
    url(r'^delete/(?P<id>([0-9]+))$', actions.Delete.as_view(),   name='page_delete'),
    url(r'^update/(?P<page_id>([0-9]+))$',   actions.Update.as_view(),   name='page_update'),

    url(r'^validation/variation/(?P<id>([0-9]+))$',          actions.ValidationVariation.as_view(),         name='page_validation'),
    url(r'^validation/disease/(?P<id>([0-9]+))$',            actions.ValidationDisease.as_view(),           name='page_validation'),
    url(r'^validation/gene/(?P<id>([0-9]+))$',               actions.ValidationGene.as_view(),              name='page_validation'),
    url(r'^validation/trait/(?P<id>([0-9]+))$',              actions.ValidationTrait.as_view(),             name='page_validation'),
    url(r'^validation/treatment/(?P<id>([0-9]+))$',          actions.ValidationTreatment.as_view(),         name='page_validation'),
    url(r'^validation$',                                     actions.Validation.as_view(),                  name='page_validation'),
    url(r'^block_approve/(?P<page>([A-Za-z0-9]+))/(?P<kind>[^/]+)/(?P<id>([0-9]+))$',   actions.BlockApprove.as_view(),   name='block_approve'),
    url(r'^block_reject/(?P<page>([A-Za-z0-9]+))/(?P<kind>[^/]+)/(?P<id>([0-9]+))$',   actions.BlockReject.as_view(),   name='block_reject'),
]
