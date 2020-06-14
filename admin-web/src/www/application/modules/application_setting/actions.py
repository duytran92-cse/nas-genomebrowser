from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from notasquare.urad_web import actions, page_contexts, widgets
from notasquare.urad_web_material import renderers
from application import constants
from . import components
from application.modules.page import components as page_components

class Update(actions.crud.UpdateAction):
    def create_page_context(self):
        return components.FullPageContext(self.params, self.container)
    def create_form(self):
        pages = page_components.PageStore(self.get_container()).populate_combobox()

        form = widgets.form.Form()
        form.set_title('Application setting')
        form.add_field(widgets.field.Textbox('application_title'))
        form.add_field(widgets.field.Richtext('contact_address_text'))
        form.add_field(widgets.field.Richtext('about_genopedia_text'))
        form.add_field(widgets.field.Textbox('facebook_url'))
        form.add_field(widgets.field.Textbox('twitter_url'))
        form.add_field(widgets.field.Textbox('youtube_url'))
        form.add_field(widgets.field.Textbox('linkedin_url'))
        form.add_field(widgets.field.Textbox('google_plus_url'))
        form.add_field(widgets.field.Combobox('impression_page', choices=pages, blank=True))
        form.add_field(widgets.field.Combobox('privacy_page', choices=pages, blank=True))
        form.add_field(widgets.field.Combobox('copyright_page', choices=pages, blank=True))
        form.add_field(widgets.field.Combobox('term_of_use_page', choices=pages, blank=True))

        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('Page information')
        form.renderer.add_field('application_title', 'Application title')
        form.renderer.add_field('contact_address_text', 'Contact address', rows=8)
        form.renderer.add_field('about_genopedia_text', 'About genopedia', rows=8)

        form.renderer.add_section('Social Networks')
        form.renderer.add_field('facebook_url', 'Facebook')
        form.renderer.add_field('twitter_url', 'Twitter')
        form.renderer.add_field('youtube_url', 'Youtube')
        form.renderer.add_field('linkedin_url', 'LinkedIn')
        form.renderer.add_field('google_plus_url', 'Google Plus')

        form.renderer.add_section('Pages')
        form.renderer.add_field('impression_page', 'Impression')
        form.renderer.add_field('privacy_page', 'Privacy')
        form.renderer.add_field('copyright_page', 'Copyright')
        form.renderer.add_field('term_of_use_page', 'Term of use')

        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('richtext', renderers.widgets.field.RichtextRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        return form
    def load_form(self, form):
        result = components.ApplicationSettingStore(self.get_container()).get()
        if result['status'] == 'ok':
            record = result['data']['record']
            form.set_form_data(record)
        else:
            form.add_message('danger', "Can't load form")
    def process_form_data(self, data):
        return components.ApplicationSettingStore(self.get_container()).update(data)
