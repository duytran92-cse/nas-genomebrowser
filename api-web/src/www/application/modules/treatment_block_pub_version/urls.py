
from django.conf.urls import include, url
from . import handlers

urlpatterns = [
    url(r'^get$',    handlers.Get.as_view(),      name='treatment_block_pub_version_get'),
    url(r'^list$',   handlers.List.as_view(),     name='treatment_block_pub_version_list'),
    url(r'^update$', handlers.Update.as_view(),   name='treatment_block_pub_version_update'),
]
