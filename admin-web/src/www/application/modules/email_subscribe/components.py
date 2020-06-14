from django.conf import settings
from application.modules.common import page_contexts

class EmailSubscribeStore(object):
    def __init__(self, container):
        self.container = container
    def list(self, params={}, sortkey='id', sortdir='desc', page_number=1):
        params['_pager_start'] = (page_number - 1) * 10
        params['_pager_num'] = 10
        params['_sort_key'] = sortkey
        params['_sort_dir'] = sortdir
        data = self.container.call_api(settings.GENOME_BROWSER_API_URL + '/email_subscribe/list', GET=params)
        return data['data']
    def get(self, id):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/email_subscribe/get', GET={'id': id})
    def create(self, data):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/email_subscribe/create', POST=data)
    def update(self, data, id):
        data['id'] = id
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/email_subscribe/update', POST=data)
    def delete(self, id):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/email_subscribe/delete', POST={'id': id})
    def populate_combobox(self, kind=''):
        choices = []
        params = {}
        if kind != '':
            params['kind'] = kind
        records = self.list(sortkey='title', sortdir='asc', params=params)
        for record in records['records']:
            choices.append({
                'id':     record['id'],
                'label':  record['title']
            })
        return choices



class FullPageContext(page_contexts.FullPageContext):
    def __init__(self, params, container):
        super(FullPageContext, self).__init__(container.request)
        self.menu.set_group_selected('email_subscribe')
