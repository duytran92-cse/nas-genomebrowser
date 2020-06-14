from django.conf import settings
from application.modules.common import page_contexts

class GeneBlockAliasVersionStore(object):
    def __init__(self, container):
        self.container = container
    def list(self, params={}, sortkey='id', sortdir='desc', page_number=1):
        params['_pager_start'] = (page_number - 1) * 10
        params['_pager_num'] = 10
        params['_sort_key'] = sortkey
        params['_sort_dir'] = sortdir
        data = self.container.call_api(settings.GENOME_BROWSER_API_URL + '/gene_block_alias_version/list', GET=params)
        return data['data']
    def get(self, alias_id):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/gene_block_alias_version/get', GET={'alias_id': alias_id})
    def update(self, data, alias_id):
        data['alias_id'] = alias_id
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/gene_block_alias_version/update', POST=data)
    def delete(self, alias_id):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/gene_block_alias_version/delete', POST={'alias_id': alias_id})
    def active(self, text_id):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/gene_block_alias_version/active', POST={'id': text_id})

class FullPageContext(page_contexts.FullPageContext):
    def __init__(self, params, container):
        super(FullPageContext, self).__init__(container.request)
        self.menu.set_group_selected('gene')
        if 'gene_id' in params:
            self.submenu.create_menu_group('summary', 'Summay', '/gene/summary/%s' % (str(params['gene_id'])), 'zmdi-border-all')
            self.submenu.create_menu_group('update', 'Update', '/gene/update/%s' % (str(params['gene_id'])), 'zmdi-border-all')
            self.submenu.create_menu_group('block', 'Block', '/gene/detail/%s/block/list' % (str(params['gene_id'])), 'zmdi-border-all')
            self.submenu.create_menu_group('comment', 'Comment', '/gene/detail/%s/comment/list' % (str(params['gene_id'])), 'zmdi-border-all')

        self.submenu.set_group_selected('block')
        if 'gene_id' in params and  'gene_block_id' in params:
            self.subsubmenu.create_menu_group('list', 'Alias Versions', '/gene/detail/%s/block/detail/%s/alias_version/list' % (str(params['gene_id']), str(params['gene_block_id'])), 'zmdi-border-all')
