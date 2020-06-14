
from django.conf.urls import include, url
from . import actions

urlpatterns = [
	url(r'^update$',   						actions.Update.as_view(),   name='treatment_block_update'),
    url(r'^view/(?P<block_id>([0-9]+))$',   actions.Update.as_view(),   	name='treatment_block_get'),
]
