from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from notasquare.urad_web import actions, page_contexts, widgets
from notasquare.urad_web_material import renderers
from application.modules.common import page_contexts, actions as common_actions, components as common_components
from application.themes.genopedia import renderers as genopedia_renderers
from application.themes.genopedia import widgets as genopedia_widgets
from application import constants
from . import components

class Update(actions.crud.UpdateAction, common_actions.BaseAction):
    def create_form(self):
        trait_block = components.TraitBlockStore(self.get_container()).get(self.params['block_id'])
        kind = trait_block['data']['record']['kind']

        form = widgets.form.Form()
        form.renderer = renderers.widgets.form.HorizontalFormRenderer()

        if kind == 'general_text':
            form.add_field(widgets.field.Textbox('title'))
            form.add_field(widgets.field.Textarea('text'))
            form.renderer.add_section('General - Text')
            form.renderer.add_field('title', 'Title')
            form.renderer.add_field('text', 'Text', rows=15)
        if kind == 'general_publications':
            form.add_field(widgets.field.List('publications', {
                'pmid':     widgets.field.Textbox('pmid'),
                'doi':      widgets.field.Textbox('doi'),
                'pmc':      widgets.field.Textbox('pmc'),
                'title':    widgets.field.Textarea('title'),
                'authors':  widgets.field.Textarea('authors'),
                'journal':  widgets.field.Textarea('journal')
            }))
            form.renderer.add_section('General - Publications')
            form.renderer.add_field('publications', 'Publications', columns=[
                {'id': 'pmid',        'label': 'PMID',       'width': '10%'},
                {'id': 'doi',         'label': 'DOI',        'width': '10%'},
                {'id': 'pmc',         'label': 'PMC',        'width': '10%'},
                {'id': 'title',       'label': 'Title',      'width': '30%'},
                {'id': 'authors',     'label': 'Authors',    'width': '15%'},
                {'id': 'journal',     'label': 'Journal',    'width': '15%'},
            ])

        if kind == 'general_alias':
            # Show effect & risk
            form.add_field(widgets.field.List('alias', {
                'id':           widgets.field.Textbox('id'),
                'alias':         widgets.field.Textbox('alias')
            }))
            form.renderer.add_section('Variation - Alias')

            form.renderer.add_field('alias', 'Alias', columns=[
                {'id': 'alias',     'label': 'Alias',   'width': '50%'}
            ])   

        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        form.renderer.set_field_renderer('list', renderers.widgets.field.ListRenderer())
        return form
    def load_form(self, form):
        result = components.TraitBlockStore(self.get_container()).get(self.params['block_id'])
        if result['status'] == 'ok':
            record = result['data']['record']
            form.set_things({
                'page': 'trait',
                'page_title': record['trait_title']
            })
            form.set_form_data(record)
        else:
            form.add_message('danger', "Can't load form")
    def process_form_data(self, data):
        data['new_version'] = True
        res = components.TraitBlockStore(self.get_container()).update(data, self.params['block_id'])
        rs = components.TraitBlockStore(self.get_container()).helper(res['data']['pk'])
        self.params['page_title'] = rs['data']['record']['title']
        return res

    def handle_on_success(self, messages):
        return HttpResponseRedirect('/trait/%s' % (self.params["page_title"]))
