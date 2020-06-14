from django.conf import settings
from application.modules.common import page_contexts

class DashboardStore(object):
    def __init__(self, container):
        self.container = container
    def list(self):
        a = self.container.call_api(settings.GENOME_BROWSER_API_URL + '/page/dashboard')
        b = self.container.call_api(settings.GENOME_BROWSER_API_URL + '/page/unstable_blocks')
        data = {}
        data['record'] = []
        for item in a['data']['record']:
            data['record'].append({
                'links': item['links']
            })
        data['record'].append({
            'records': b['data']['record']['records']
        })
        return data

class FullPageContext(page_contexts.FullPageContext):
    def __init__(self, params, container):
        super(FullPageContext, self).__init__(container.request)
        self.menu.set_group_selected('dashboard')
        