from django.conf import settings
from application.modules.common import page_contexts

class VariationBlockInfoboxVersionStore(object):
    def __init__(self, container):
        self.container = container
    def list(self, params={}, sortkey='id', sortdir='desc', page_number=1):
        params['_pager_start'] = (page_number - 1) * 10
        params['_pager_num'] = 10
        params['_sort_key'] = sortkey
        params['_sort_dir'] = sortdir
        data = self.container.call_api(settings.GENOME_BROWSER_API_URL + '/variation_block_infobox_version/list', GET=params)
        return data['data']
    def get(self, infobox_id):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/variation_block_infobox_version/get', GET={'infobox_id': infobox_id})
    def update(self, data, infobox_id):
        data['infobox_id'] = infobox_id
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/variation_block_infobox_version/update', POST=data)
    def delete(self, infobox_id):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/variation_block_infobox_version/delete', POST={'infobox_id': infobox_id})
    def active(self, text_id):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/variation_block_infobox_version/active', POST={'id': text_id})


class FullPageContext(page_contexts.FullPageContext):
    def __init__(self, params, container):
        super(FullPageContext, self).__init__(container.request)
        self.menu.set_group_selected('variation')
        if 'variation_id' in params:
            self.submenu.create_menu_group('summary', 'Summary', '/variation/summary/%s' % (str(params['variation_id'])), 'zmdi-border-all')
            self.submenu.create_menu_group('update', 'Update', '/variation/update/%s' % (str(params['variation_id'])), 'zmdi-border-all')
            self.submenu.create_menu_group('block', 'Block', '/variation/detail/%s/block/list' % (str(params['variation_id'])), 'zmdi-border-all')
            self.submenu.create_menu_group('comment', 'Comment', '/variation/detail/%s/comment/list' % (str(params['variation_id'])), 'zmdi-border-all')

        self.submenu.set_group_selected('block')
        if 'variation_id' in params and  'variation_block_id' in params:
            self.subsubmenu.create_menu_group('list', 'Infobox Versions', '/variation/detail/%s/block/detail/%s/infobox_version/list' % (str(params['variation_id']), str(params['variation_block_id'])), 'zmdi-border-all')
