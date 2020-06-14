
from django.conf.urls import include, url
from . import handlers

urlpatterns = [
    url(r'^get$',    handlers.Get.as_view(),      name='trait_get'),
    url(r'^view$',    handlers.View.as_view(),      name='trait_view'),
    url(r'^list$',   handlers.List.as_view(),     name='trait_list'),
    url(r'^create$',    handlers.Create.as_view(),      name='trait_create'),
    url(r'^update$',   handlers.Update.as_view(),     name='trait_update'),
    url(r'^delete$',    handlers.Delete.as_view(),      name='trait_delete'),
    url(r'^summary$',    handlers.Summary.as_view(),      name='trait_summary')
]
