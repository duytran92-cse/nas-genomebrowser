
from django.conf.urls import include, url
from . import handlers

urlpatterns = [
    url(r'^$',          handlers.Create.as_view(),      name='email_subscribe_create'),
    url(r'^get$',       handlers.Get.as_view(),         name='email_subscribe_get'),
    url(r'^list$',      handlers.List.as_view(),        name='email_subscribe_list'),
    url(r'^create$',    handlers.Create.as_view(),      name='email_subscribe_create'),
    url(r'^update$',    handlers.Update.as_view(),      name='email_subscribe_update'),
    url(r'^delete$',    handlers.Delete.as_view(),      name='email_subscribe_delete'),
]
