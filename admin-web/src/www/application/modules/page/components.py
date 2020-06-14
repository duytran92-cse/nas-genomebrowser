from django.conf import settings
from application.modules.common import page_contexts

class PageStore(object):
    def __init__(self, container):
        self.container = container
    def list(self, params={}, sortkey='id', sortdir='desc', page_number=1):
        params['_pager_start'] = (page_number - 1) * 10
        params['_pager_num'] = 10
        params['_sort_key'] = sortkey
        params['_sort_dir'] = sortdir
        data = self.container.call_api(settings.GENOME_BROWSER_API_URL + '/page/list', GET=params)
        return data['data']
    def get(self, id):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/page/get', GET={'id': id})
    def create(self, data):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/page/create', POST=data)
    def update(self, data, id):
        data['id'] = id
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/page/update', POST=data)
    def delete(self, id):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/page/delete', POST={'id': id})
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
    def list_blocks(self):
        data = self.container.call_api(settings.GENOME_BROWSER_API_URL + '/page/list_blocks')
        return data['data']
    def get_blocks_variation(self, id):
        data = self.container.call_api(settings.GENOME_BROWSER_API_URL + '/page/get_blocks_variation', GET={'id': id})
        return data['data']
    def get_blocks_gene(self, id):
        data = self.container.call_api(settings.GENOME_BROWSER_API_URL + '/page/get_blocks_gene', GET={'id': id})
        return data['data']
    def get_blocks_disease(self, id):
        data = self.container.call_api(settings.GENOME_BROWSER_API_URL + '/page/get_blocks_disease', GET={'id': id})
        return data['data']
    def get_blocks_trait(self, id):
        data = self.container.call_api(settings.GENOME_BROWSER_API_URL + '/page/get_blocks_trait', GET={'id': id})
        return data['data']
    def get_blocks_treatment(self, id):
        data = self.container.call_api(settings.GENOME_BROWSER_API_URL + '/page/get_blocks_treatment', GET={'id': id})
        return data['data']
    def block_stable_update(self, params):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/page/block_stable_update', POST={'params': params})


class FullPageContext(page_contexts.FullPageContext):
    def __init__(self, params, container):
        super(FullPageContext, self).__init__(container.request)
        self.menu.set_group_selected('page')
        if 'page_id' in params:
            self.submenu.create_menu_group('update', 'Update', '/page/update/%s' % (str(params['page_id'])), 'zmdi-border-all')
            self.submenu.create_menu_group('block', 'Block', '/page/detail/%s/block/list' % (str(params['page_id'])), 'zmdi-border-all')
            self.submenu.create_menu_group('comment', 'Comment', '/page/detail/%s/comment/list' % (str(params['page_id'])), 'zmdi-border-all')
