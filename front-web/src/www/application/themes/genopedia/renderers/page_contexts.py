from django.template import loader
from notasquare.urad_web.renderers import BaseRenderer

class FullPageContextRenderer(BaseRenderer):
    def __init__(self):
        super(FullPageContextRenderer, self).__init__()
        self.template = 'genopedia/page_contexts/full.html'
    def render(self, full_page_context):
        template = loader.get_template(self.template)
        context = {
            'app_title':        full_page_context.app_title,
            'page_title':       full_page_context.page_title,
            'menu':             full_page_context.menu,
            'submenu':          full_page_context.submenu,
            'breadcrumb':       full_page_context.breadcrumb,
            'texts': {
                'contact_us':         full_page_context.contact_us_text,
                'about_genopedia':    full_page_context.about_genopedia_text,
            },
            'social_network_url': {
                'facebook':           full_page_context.facebook_url,
                'twitter':            full_page_context.twitter_url,
                'youtube':            full_page_context.youtube_url,
                'linkedin':           full_page_context.linkedin_url,
                'google_plus':        full_page_context.google_plus_url,
            },
            'frontSetting': {
                'impressionUrl':           full_page_context.impressionUrl,
                'termOfUseUrl':            full_page_context.termOfUseUrl,
                'privacyPolicyUrl':        full_page_context.privacyPolicyUrl,
                'copyrightUrl':            full_page_context.copyrightUrl,
            },
            'genebay_url':              full_page_context.genebay_url,
            'user_url':                 full_page_context.user_url,
            'lang':                     full_page_context.lang,
            'textblock':                full_page_context.textblock,
            'user_name':                full_page_context.user_name,
            'user_photo':               full_page_context.user_photo,
            'logout':                   full_page_context.user_logout,
            'login':                    full_page_context.user_login,
            'sign_up':                  full_page_context.user_sign_up,
            'private_result':            full_page_context.private_result,
            'science_filter':            full_page_context.science_filter,
            'url_upload':                full_page_context.url_upload,
            'url_filter':                full_page_context.url_filter
        }

        widget_html = ''
        for widget in full_page_context.widgets:
            widget_html += widget.render()
        context['widget_html'] = widget_html

        return template.render(context)
