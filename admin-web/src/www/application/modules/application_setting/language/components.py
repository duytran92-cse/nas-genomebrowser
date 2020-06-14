from django.conf import settings
from application.modules.common import page_contexts

class LanguageStore(object):
    def __init__(self, container):
        self.container = container
    def list(self, params={}, sortkey='id', sortdir='desc', page_number=1):
        params['_pager_start'] = (page_number - 1) * 10
        params['_pager_num'] = 10
        params['_sort_key'] = sortkey
        params['_sort_dir'] = sortdir
        data = self.container.call_api(settings.GENOME_BROWSER_API_URL + '/language/list', GET=params)
        return data['data']
    def get(self, id):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/language/get', GET={'id': id})
    def create(self, data):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/language/create', POST=data)
    def update(self, data, id):
        data['id'] = id
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/language/update', POST=data)
    def delete(self, id):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/language/delete', POST={'id': id})
    def populate_combobox(self):
        choices = []
        params = {}
        params['_sort_key'] = 'title'
        params['_sort_dir'] = 'asc'
        records = self.container.call_api(settings.GENOME_BROWSER_API_URL + '/language/list', GET=params)
        for record in records['data']['records']:
            choices.append({
                'id':     record['code'],
                'label':  record['title']
            })
        return choices

class FullPageContext(page_contexts.FullPageContext):
    def __init__(self, params, container):
        super(FullPageContext, self).__init__(container.request)
        self.menu.set_group_selected('application_setting')
        self.submenu.set_group_selected('language')
        self.submenu.create_menu_group('text_block', 'Text Blocks', '/text_block/list', 'zmdi-border-all')
        self.submenu.create_menu_group('language', 'Languages', '/language/list', 'zmdi-border-all')
