from django.conf import settings
from application.modules.common import page_contexts

class TraitStore(object):
    def __init__(self, container):
        self.container = container
    def list(self, params={}, sortkey='id', sortdir='desc', page_number=1):
        params['_pager_start'] = (page_number - 1) * 10
        params['_pager_num'] = 10
        params['_sort_key'] = sortkey
        params['_sort_dir'] = sortdir
        data = self.container.call_api(settings.GENOME_BROWSER_API_URL + '/trait/list', GET=params)
        return data['data']
    def get(self, id):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/trait/get', GET={'id': id})
    def create(self, data):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/trait/create', POST=data)
    def update(self, data, id):
        data['id'] = id
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/trait/update', POST=data)
    def delete(self, id):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/trait/delete', POST={'id': id})
    def populate_combobox(self, kind=''):
        choices = []
        params = {}
        if kind != '':
            params['kind'] = kind
        params['_sort_key'] = 'title'
        params['_sort_dir'] = 'asc'
        records = self.container.call_api(settings.GENOME_BROWSER_API_URL + '/trait/list', GET=params)
        for record in records['records']:
            choices.append({
                'id':     record['id'],
                'label':  record['title']
            })
        return choices
    def summary(self, id):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/trait/summary', GET={'trait_id': id})


class FullPageContext(page_contexts.FullPageContext):
    def __init__(self, params, container):
        super(FullPageContext, self).__init__(container.request)
        self.menu.set_group_selected('trait')
        if 'trait_id' in params:
            self.submenu.create_menu_group('summary', 'Summay', '/trait/summary/%s' % (str(params['trait_id'])), 'zmdi-border-all')
            self.submenu.create_menu_group('update', 'Update', '/trait/update/%s' % (str(params['trait_id'])), 'zmdi-border-all')
            self.submenu.create_menu_group('block', 'Block', '/trait/detail/%s/block/list' % (str(params['trait_id'])), 'zmdi-border-all')
            self.submenu.create_menu_group('comment', 'Comment', '/trait/detail/%s/comment/list' % (str(params['trait_id'])), 'zmdi-border-all')

