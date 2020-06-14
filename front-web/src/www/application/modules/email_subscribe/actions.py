from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from application.modules.common import page_contexts, actions as common_actions, components as common_components
from . import components

class EmailSubcibe(common_actions.BaseAction):
    def POST(self):
        rs = components.EmailSubcribeStore(self.get_container()).email_subscribe(self.params)
        return JsonResponse(rs)
