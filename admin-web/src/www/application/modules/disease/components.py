from django.conf import settings
from application.modules.common import page_contexts

class DiseaseStore(object):
    def __init__(self, container):
        self.container = container
    def list(self, params={}, sortkey='id', sortdir='desc', page_number=1):
        params['_pager_start'] = (page_number - 1) * 10
        params['_pager_num'] = 10
        params['_sort_key'] = sortkey
        params['_sort_dir'] = sortdir
        data = self.container.call_api(settings.GENOME_BROWSER_API_URL + '/disease/list', GET=params)
        return data['data']
    def get(self, id):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/disease/get', GET={'id': id})
    def create(self, data):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/disease/create', POST=data)
    def update(self, data, id):
        data['id'] = id
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/disease/update', POST=data)
    def delete(self, id):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/disease/delete', POST={'id': id})
    def populate_combobox(self, kind=''):
        choices = []
        params = {}
        if kind != '':
            params['kind'] = kind
        params['_sort_key'] = 'title'
        params['_sort_dir'] = 'asc'
        records = self.container.call_api(settings.GENOME_BROWSER_API_URL + '/disease/list', GET=params)
        for record in records['records']:
            choices.append({
                'id':     record['id'],
                'label':  record['title']
            })
        return choices
    def summary(self, id):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/disease/summary', GET={'disease_id': id})


class FullPageContext(page_contexts.FullPageContext):
    def __init__(self, params, container):
        super(FullPageContext, self).__init__(container.request)
        self.menu.set_group_selected('disease')
        if 'disease_id' in params:
            self.submenu.create_menu_group('summary', 'Summay', '/disease/summary/%s' % (str(params['disease_id'])), 'zmdi-border-all')
            self.submenu.create_menu_group('update', 'Update', '/disease/update/%s' % (str(params['disease_id'])), 'zmdi-border-all')
            self.submenu.create_menu_group('block', 'Block', '/disease/detail/%s/block/list' % (str(params['disease_id'])), 'zmdi-border-all')
            self.submenu.create_menu_group('comment', 'Comment', '/disease/detail/%s/comment/list' % (str(params['disease_id'])), 'zmdi-border-all')
