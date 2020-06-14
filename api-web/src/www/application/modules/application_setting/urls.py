
from django.conf.urls import include, url
from . import handlers

urlpatterns = [
    url(r'^get$',    handlers.Get.as_view(),      name='application_setting_get'),
    url(r'^update$', handlers.Update.as_view(),   name='application_setting_update'),
]
