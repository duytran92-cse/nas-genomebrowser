from django.conf import settings
from application.modules.common import page_contexts

class TreatmentBlockPublicationVersionStore(object):
    def __init__(self, container):
        self.container = container
    def list(self, params={}, sortkey='id', sortdir='desc', page_number=1):
        params['_pager_start'] = (page_number - 1) * 10
        params['_pager_num'] = 10
        params['_sort_key'] = sortkey
        params['_sort_dir'] = sortdir
        data = self.container.call_api(settings.GENOME_BROWSER_API_URL + '/treatment_block_pub_version/list', GET=params)
        return data['data']
    def get(self, pub_id):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/treatment_block_pub_version/get', GET={'pub_id': pub_id})
    def update(self, data, pub_id):
        data['pub_id'] = pub_id
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/treatment_block_pub_version/update', POST=data)
    def delete(self, pub_id):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/treatment_block_pub_version/delete', POST={'pub_id': pub_id})
    def active(self, text_id):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/treatment_block_eff_version/active', POST={'id': text_id})

class FullPageContext(page_contexts.FullPageContext):
    def __init__(self, params, container):
        super(FullPageContext, self).__init__(container.request)
        self.menu.set_group_selected('treatment')
        if 'treatment_id' in params:
            self.submenu.create_menu_group('summary', 'Summay', '/treatment/summary/%s' % (str(params['treatment_id'])), 'zmdi-border-all')
            self.submenu.create_menu_group('update', 'Update', '/treatment/update/%s' % (str(params['treatment_id'])), 'zmdi-border-all')
            self.submenu.create_menu_group('block', 'Block', '/treatment/detail/%s/block/list' % (str(params['treatment_id'])), 'zmdi-border-all')
            self.submenu.create_menu_group('comment', 'Comment', '/treatment/detail/%s/comment/list' % (str(params['treatment_id'])), 'zmdi-border-all')

        self.submenu.set_group_selected('block')
        if 'treatment_id' in params and  'treatment_block_id' in params:
            self.subsubmenu.create_menu_group('list', 'Publication Versions', '/treatment/detail/%s/block/detail/%s/pub_version/list' % (str(params['treatment_id']), str(params['treatment_block_id'])), 'zmdi-border-all')
