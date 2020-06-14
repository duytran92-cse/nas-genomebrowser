
from django.conf.urls import include, url
from . import handlers

urlpatterns = [
    url(r'^get$',    handlers.Get.as_view(),      name='variation_block_get'),
    url(r'^list$',   handlers.List.as_view(),     name='variation_block_list'),
    url(r'^create$', handlers.Create.as_view(),   name='variation_block_create'),
    url(r'^update$', handlers.Update.as_view(),   name='variation_block_update'),
    url(r'^save_text_eff$', handlers.SaveTextEff.as_view(),   name='variation_block_update'),
    url(r'^delete$', handlers.Delete.as_view(),   name='variation_block_delete'),
    url(r'^helper$', handlers.Helper.as_view(),   name='variation_block_helper'),
]
