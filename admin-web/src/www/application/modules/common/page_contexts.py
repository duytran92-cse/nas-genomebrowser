import urllib
from django.conf import settings
from notasquare.urad_web.page_contexts import standard
from notasquare.urad_web_material import renderers
from application.modules.user.manager import UserManager

class FullPageContext(standard.FullPageContext):
    def __init__(self,request):
        super(FullPageContext, self).__init__()
        self.app_title = 'Genome browser'
        self.page_title = 'Genome browser'
        self.breadcrumb.add_entry('home', 'Dashboard', '/')
        self.menu.create_menu_group('dashboard', 'Dashboard', '/dashboard', 'zmdi-format-subject')
        self.menu.create_menu_group('email_subscribe', 'Email subscribe', '/email_subscribe/', 'zmdi-format-subject')
        self.menu.create_menu_group('variation', 'Variation', '/variation/list', 'zmdi-format-subject')
        self.menu.create_menu_group('gene', 'Gene', '/gene/list', 'zmdi-format-subject')
        self.menu.create_menu_group('disease', 'Disease', '/disease/list', 'zmdi-format-subject')
        self.menu.create_menu_group('trait', 'Trait', '/trait/list', 'zmdi-format-subject')
        self.menu.create_menu_group('treatment', 'Treatment', '/treatment/list', 'zmdi-format-subject')
        self.menu.create_menu_group('page', 'Page', '/page/list', 'zmdi-format-subject')
        self.menu.create_menu_group('application_setting', 'Setting', '/application_setting/update', 'zmdi-format-subject')
        self.renderer = renderers.page_contexts.FullPageContextRenderer()

        # User
        self.user = request.META['USER']
        self.user['logout_link'] = settings.SECURITY_SERVER_URL + '/user/logout?redirect=%s' % (settings.APPLICATION_URL)
