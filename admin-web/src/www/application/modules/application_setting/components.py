from django.conf import settings
from application.modules.common import page_contexts

class ApplicationSettingStore(object):
    def __init__(self, container):
        self.container = container
    def get(self):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/application_setting/get', GET={})
    def update(self, data):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/application_setting/update', POST=data)


class FullPageContext(page_contexts.FullPageContext):
    def __init__(self, params, container):
        super(FullPageContext, self).__init__(container.request)
        self.menu.set_group_selected('application_setting')
        self.submenu.create_menu_group('text_block', 'Text Blocks', '/text_block/list', 'zmdi-border-all')
        self.submenu.create_menu_group('language', 'Languages', '/language/list', 'zmdi-border-all')