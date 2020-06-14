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
        variation_block = components.VariationBlockStore(self.get_container()).get(self.params['block_id'])
        kind = variation_block['data']['record']['kind']
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
        if kind == 'variation_infobox':
            form.add_field(widgets.field.List('infobox', {
                'key':     widgets.field.Textbox('key'),
                'value':      widgets.field.Textarea('value')
            }))
            form.renderer.add_section('Variation - Infobox')
            form.renderer.add_field('infobox', 'Infobox', columns=[
                {'id': 'key',        'label': 'KEY',       'width': '20%'},
                {'id': 'value',      'label': 'VALUE',     'width': '60%'}
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

        if kind == 'general_disgenet_diseases':

            form.add_field(widgets.field.List('disgenet_diseases', {
                'id':           widgets.field.Textbox('id'),
                'title':        widgets.field.Textbox('title'),
                'pubmedid':     widgets.field.Textbox('pubmedid')
            }))
            form.renderer.add_section('Variation - Associated Diseases')

            form.renderer.add_field('disgenet_diseases', 'Associated diseases', columns=[
                {'id': 'title',             'label': 'Disease',   'width': '30%'},
                {'id': 'pubmedid',          'label': 'Pubmedid',   'width': '30%'}
            ])
        if kind == 'variation_pub_text':
            form.add_field(widgets.field.List('pub_text', {
                'id':               widgets.field.Textbox('id'),
                'title':            widgets.field.Textbox('title'),
                'pubmedid':         widgets.field.Textbox('pubmedid'),
                'sentence':         widgets.field.Textarea('sentence'),
            }))
            form.renderer.add_section('Variation - Publications Text')

            form.renderer.add_field('pub_text', 'Publications Text', columns=[
                {'id': 'pubmedid',          'label': 'Pubmedid',    'width': '10%'},
                {'id': 'title',             'label': 'Title',       'width': '20%'},
                {'id': 'sentence',          'label': 'Sentence',    'width': '70%', 'rows': 15},
            ])
        if kind == 'variation_effect':
            form.renderer.add_section('Variation - Effect')
            form.add_field(widgets.field.ListInfo('genotypes', {
                'id':           widgets.field.Textbox('id'),
                'genotype_eff':     widgets.field.Textbox('genotype_eff'),
                'box_color':    widgets.field.Textbox('box_color'),
                'source':       widgets.field.Textarea('source'),
            }))

            form.renderer.add_field('genotypes', 'Genotypes', columns=[
                {'id': 'genotype_eff','label': 'Genotype',  'width': '10%'},
                {'id': 'box_color',   'label': 'Box color', 'width': '10%'},
                {'id': 'source',      'label': 'Information','width': '70%', 'title': "Web link showing where this information came from"}
            ])
            genotype = components.VariationBlockStore(self.get_container()).get_genotype(variation_block['data']['record']['variation_id'])
            eff_note = components.VariationBlockStore(self.get_container()).get_eff_note()['records'][0]
            form.add_field(widgets.field.ListInfo('risks', {
                'popcode':      widgets.field.Combobox('popcode', choices=constants.POPULATION_CODES_EFFECT),
                'genotype':     widgets.field.Combobox('genotype', choices=genotype['records']),
                'risk':         widgets.field.Textarea('risk'),
                'odd_ratio':    widgets.field.Textbox('odd_ratio'),
                'evidences':    widgets.field.Textarea('evidences'),
                'pmid':         widgets.field.Textbox('pmid')
            }))
            form.renderer.add_field('risks', 'Add a new effect for a genetic variation', columns=[
                {'id': 'popcode',     'label': 'Population studied',   'width': '10%', 'edit': True, 'title': eff_note.get('popcode', '')},
                {'id': 'genotype',    'label': 'Genotype',  'width': '10%', 'edit': True, 'title': eff_note.get('genotype', '')},
                {'id': 'risk',        'label': 'Risk',      'width': '25%', 'edit': True, 'title': eff_note.get('risk', '')},
                {'id': 'odd_ratio',   'label': 'Odd ratio', 'width': '10%', 'edit': True, 'title': eff_note.get('odd_ratio', '')},
                {'id': 'evidences',   'label': 'Evidences', 'width': '25%', 'edit': True, 'title': eff_note.get('evidences', '')},
                {'id': 'pmid',        'label': 'PMID',      'width': '10%', 'edit': True, 'title': eff_note.get('pmid', '')},
            ])
        if kind == 'variation_frequency':
            form.add_field(widgets.field.List('frequencies', {
                'id':                   widgets.field.Textbox('id'),
                'popcode':              widgets.field.Combobox('popcode', choices=constants.POPULATION_CODES),
                'genotype_count_00':    widgets.field.Textbox('genotype_count_00'),
                'genotype_count_01':    widgets.field.Textbox('genotype_count_01'),
                'genotype_count_11':    widgets.field.Textbox('genotype_count_11')
            }))
            form.renderer.add_section('Variation - Frequency')
            form.renderer.add_field('frequencies', 'Frequencies', columns=[
                {'id': 'popcode',               'label': 'Popcode',             'width': '20%'},
                {'id': 'genotype_count_00',     'label': 'Genotype_count_00',   'width': '20%'},
                {'id': 'genotype_count_01',     'label': 'Genotype_count_01',   'width': '20%'},
                {'id': 'genotype_count_11',     'label': 'Genotype_count_11',   'width': '20%'}
            ])

        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        form.renderer.set_field_renderer('list', renderers.widgets.field.ListRenderer())
        form.renderer.set_field_renderer('list_info', renderers.widgets.field.ListInfoRenderer())
        return form
    def load_form(self, form):
        result = components.VariationBlockStore(self.get_container()).get(self.params['block_id'])
        if result['status'] == 'ok':
            record = result['data']['record']
            form.set_things({
                'page': 'variation',
                'page_title': record['variation_title']
            })
            self.params['page_title'] = record['variation_title']
            form.set_form_data(record)
        else:
            form.add_message('danger', "Can't load form")
    def process_form_data(self, data):
        data['new_version'] = True
        res = components.VariationBlockStore(self.get_container()).update(data, self.params['block_id'])
        rs = components.VariationBlockStore(self.get_container()).helper(res['data']['pk'])
        self.params['page_title'] = rs['data']['record']['title']
        return res

    def handle_on_success(self, messages):
        return HttpResponseRedirect('/variation/%s' % (self.params["page_title"]))

class SaveTextEff(common_actions.BaseAction):
    def POST(self):
        rs = components.VariationBlockStore(self.get_container()).save_text_eff(self.params)
        return JsonResponse(rs)
