from notasquare.urad_web.page_contexts import standard
from application.themes.genopedia import renderers
from application.modules.common import components as common_components
from django.conf import settings

class FullPageContext(standard.FullPageContext):
    def __init__(self):
        super(FullPageContext, self).__init__()
        self.app_title = 'Genopedia'
        self.page_title = 'Genopedia'
        self.menu.create_menu_group('variation', 'Variation', '/variation/list', 'zmdi-format-subject')
        self.menu.create_menu_group('gene', 'Gene', '/gene/list', 'zmdi-format-subject')
        self.menu.create_menu_group('disease', 'Disease', '/disease/list', 'zmdi-format-subject')
        self.renderer = renderers.page_contexts.FullPageContextRenderer()

        self.contact_us_text = ''
        self.about_genopedia_text = ''
        self.facebook_url = '#'
        self.twitter_url = '#'
        self.youtube_url = '#'
        self.linkedin_url = '#'
        self.google_plus_url = '#'

        self.impressionUrl = ''
        self.termOfUseUrl = ''
        self.privacyPolicyUrl = ''
        self.copyrightUrl = ''

        self.genebay_url = settings.GENEBAY_FRONTEND_URL
        self.user_url = settings.GENOPEDIA_USER_URL
        self.user_name = ''
        self.user_id       = ''
        self.user_photo = ''
        self.user_logout = ''
        self.user_login  = ''
        self.user_sign_up = ''
        self.private_result = ''
        self.science_filter= ''
        self.url_upload=''
        self.url_filter= ''
