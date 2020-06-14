
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^create$',                  actions.Create.as_view(),     name='file_upload_create'),
    url(r'^download$',                actions.Download.as_view(),   name='file_upload_download'),
]

