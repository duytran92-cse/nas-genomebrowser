from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from notasquare.urad_web import actions, widgets
from application.themes.genopedia import renderers
from application.modules.common import page_contexts, components as common_components
from application import constants
import urllib

class BaseAction(actions.BaseAction):
    def create_page_context(self):
        page_context = page_contexts.FullPageContext()
        current_url = 'http' + ('', 's')[self.request.is_secure()] + '://'+ self.request.META['HTTP_HOST']+ self.request.META['REQUEST_URI']
        record = common_components.ApplicationSettingStore(self.get_container()).get()
        application_setting = record['data']['record']

        page_context.contact_us_text = application_setting['contact_address_text']
        page_context.about_genopedia_text = application_setting['about_genopedia_text']
        page_context.facebook_url = application_setting['facebook_url']
        page_context.twitter_url = application_setting['twitter_url']
        page_context.youtube_url = application_setting['youtube_url']
        page_context.linkedin_url = application_setting['linkedin_url']
        page_context.google_plus_url = application_setting['google_plus_url']
        page_context.genebay_url = settings.GENEBAY_FRONTEND_URL
        page_context.user_url = settings.GENOPEDIA_USER_URL
        page_context.impressionUrl = '/impression'
        page_context.termOfUseUrl = '/term-of-use'
        page_context.privacyPolicyUrl = '/privacy'
        page_context.copyrightUrl = '/copyright'
        page_context.lang = self.request.session['lang']
        page_context.user_name     = ''
        page_context.user_id       = ''
        page_context.user_photo    = ''
        page_context.user_logout   = settings.GENOPEDIA_USER_URL+'/sign-out?redirect='+urllib.quote_plus(current_url)
        page_context.user_login    = settings.GENOPEDIA_USER_URL+'/sign-in?redirect='+urllib.quote_plus(current_url)
        page_context.user_sign_up    = settings.GENOPEDIA_USER_URL+'/sign-up?redirect='+urllib.quote_plus(current_url)

        user = common_components.UserManager().parse_user(self.request);
        if user != False:
            page_context.user_name     = user['username']
            page_context.user_id       = user['userid']
            page_context.user_photo    = user['photo']
            page_context.private_result = user['private_result']
            page_context.science_filter = user['science_filter']
            page_context.url_upload =  settings.GENOPEDIA_USER_URL+'/user/upload'
            page_context.url_filter =  settings.GENOPEDIA_USER_URL+'/user/science-filter'

        # Set textblock by language
        _text = common_components.PageStore(self.get_container()).get_lang_text(self.request.session['lang'])
        page_context.textblock = _text['record']

        return page_context
