
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^list$',                             actions.List.as_view(),   name='treatment_list'),
    url(r'^(?P<treatment_name>([a-zA-Z0-9- ]+))$',   actions.View.as_view(),   name='treatment_view'),    
]
