
from django.conf.urls import include, url
from . import actions

urlpatterns = [
	url(r'^save_effect_text$',   			actions.SaveTextEff.as_view(),   name='variation_block_update'), 
    url(r'^update$',   						actions.Update.as_view(),   name='variation_block_update'),
    url(r'^view/(?P<block_id>([0-9]+))$',   actions.Update.as_view(),   	name='variation_block_get'),
]
