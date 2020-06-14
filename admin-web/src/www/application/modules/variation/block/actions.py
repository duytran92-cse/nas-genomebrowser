from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from notasquare.urad_web import actions, page_contexts, widgets
from notasquare.urad_web_material import renderers
from application import constants
from application.modules.variation import components as variation_components
from . import components

class List(actions.crud.ListAction):
    def create_page_context(self):
        return variation_components.FullPageContext(self.params, self.container)
    class TableRenderer(renderers.widgets.table.DataTableRenderer):
        def render_cell_actions(self, table, row):
            html  = '<div class="btn-group btn-group">'
            html += '<a class="btn btn-xs btn-primary" href="/variation/detail/%s/block/update/%s">Edit</a>' % (row['variation'], row['id'])
            html += '<a class="btn btn-xs btn-danger" href="/variation/detail/%s/block/delete/%s" onclick="return confirm(\'Are you really want to delete this?\')">Delete</a>'  % (row['variation'], row['id'])
            if row['kind'] == 'general_text':
                html += '    <a class="btn btn-xs btn-info" href="/variation/detail/%s/block/detail/%s/version/list">Versions</a>' % (row['variation'], row['id'])
            elif row['kind'] == 'general_publications':
                html += '    <a class="btn btn-xs btn-info" href="/variation/detail/%s/block/detail/%s/pub_version/list">Versions</a>' % (row['variation'], row['id'])
            elif row['kind'] == 'variation_effect':
                html += '    <a class="btn btn-xs btn-info" href="/variation/detail/%s/block/detail/%s/eff_version/list">Versions</a>' % (row['variation'], row['id'])
            elif row['kind'] == 'variation_frequency':
                html += '    <a class="btn btn-xs btn-info" href="/variation/detail/%s/block/detail/%s/fre_version/list">Versions</a>' % (row['variation'], row['id'])
            elif row['kind'] == 'variation_infobox':
                html += '    <a class="btn btn-xs btn-info" href="/variation/detail/%s/block/detail/%s/infobox_version/list">Versions</a>' % (row['variation'], row['id'])
            elif row['kind'] == 'general_alias':
                html += '    <a class="btn btn-xs btn-info" href="/variation/detail/%s/block/detail/%s/alias_version/list">Versions</a>' % (row['variation'], row['id'])
            elif row['kind'] == 'general_disgenet_diseases':
                html += '    <a class="btn btn-xs btn-info" href="/variation/detail/%s/block/detail/%s/disgenet_diseases_version/list">Versions</a>' % (row['variation'], row['id'])
            elif row['kind'] == 'variation_pub_text':
                html += '    <a class="btn btn-xs btn-info" href="/variation/detail/%s/block/detail/%s/pub_text_version/list">Versions</a>' % (row['variation'], row['id'])
            html += '</div>'
            return html
    def create_table(self):
        table = widgets.table.DataTable()
        table.set_title('Blocks')
        table.set_subtitle('List of variation blocks')
        table.create_button('create', '/variation/detail/%s/block/create' % (self.params['variation_id']), 'zmdi-plus')
        table.create_column('id', 'ID', '7%', sortable=True)
        table.create_column('kind', 'Kind', '10%', sortable=True)
        table.create_column('position', 'Position', '10%', sortable=True)
        table.create_column('title', 'Title', '20%')
        table.create_column('sort_order', 'Sort order', '10%', sortable=True)
        table.create_column('active_version', 'Active version', '12%', sortable=False)
        table.create_column('latest_version', 'Latest version', '12%', sortable=False)
        table.create_column('actions', '', '16%')
        table.add_field(widgets.field.Textbox('text'))
        table.renderer = self.TableRenderer()
        table.renderer.table_form_renderer = renderers.widgets.form.TableFormRenderer()
        table.renderer.table_form_renderer.add_field('text', 'Text', colspan=12)
        table.renderer.table_form_renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        return table
    def load_table_data(self, table_form_data, sortkey, sortdir, page_number):
        table_form_data['variation_id'] = self.params['variation_id']
        return components.VariationBlockStore(self.get_container()).list(table_form_data, sortkey, sortdir, page_number)


class Create(actions.crud.CreateAction):
    def create_page_context(self):
        return variation_components.FullPageContext(self.params, self.container)
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('Variation block')
        form.add_field(widgets.field.Combobox('kind', choices=constants.VARIATION_BLOCK_KINDS))
        form.add_field(widgets.field.Combobox('position', choices=constants.PAGE_BLOCK_POSITIONS))
        form.add_field(widgets.field.Textbox('sort_order'))
        form.add_field(widgets.field.Textbox('title'))
        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('Variation block')
        form.renderer.add_field('kind', 'Kind')
        form.renderer.add_field('position', 'Position')
        form.renderer.add_field('sort_order', 'Sort order')
        form.renderer.add_field('title', 'Title')
        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        return form
    def load_form(self, form):
        form.set_form_data({
        })
    def process_form_data(self, data):
        data['variation_id'] = self.params['variation_id']
        res = components.VariationBlockStore(self.get_container()).create(data)
        self.params['id'] = res['data']['pk']
        return res
    def handle_on_success(self, messages):
        return HttpResponseRedirect('/variation/detail/%s/block/update/%s' % (self.params['variation_id'],self.params['id']))


class Update(actions.crud.UpdateAction):
    def create_page_context(self):
        return variation_components.FullPageContext(self.params, self.container)
    def create_form(self):
        variation_block = components.VariationBlockStore(self.get_container()).get(self.params['id'])
        kind = variation_block['data']['record']['kind']

        form = widgets.form.Form()
        form.set_title('Variation block')
        form.add_field(widgets.field.Combobox('position', choices=constants.PAGE_BLOCK_POSITIONS))
        form.add_field(widgets.field.Textbox('sort_order'))
        form.add_field(widgets.field.Textbox('title'))
        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('Add new variation block version')
        form.renderer.add_field('position', 'Position')
        form.renderer.add_field('sort_order', 'Sort order')
        form.renderer.add_field('title', 'Title')
        if kind == 'general_text':
            form.add_field(widgets.field.Textarea('text'))
            form.renderer.add_section('General - Text')
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
        if kind == 'general_disgenet_diseases':
            # Show disgenet_diseases
            form.add_field(widgets.field.List('disgenet_diseases', {
                'pubmedid':         widgets.field.Textbox('pubmedid'),
                'title':            widgets.field.Textbox('title')
            }))
            form.renderer.add_section('General - Associated Diseases')
            form.renderer.add_field('disgenet_diseases', 'Disgenet diseases', columns=[
                {'id': 'pubmedid',        'label': 'PUBMEDID',       'width': '30%'},
                {'id': 'title',           'label': 'Title',          'width': '30%'}
            ])

        if kind == 'variation_effect':
            genotype = components.DataHelper(self.get_container()).get_genotype(self.params['variation_id'])
            form.add_field(widgets.field.List('risks', {
                'popcode':      widgets.field.Combobox('popcode', choices=constants.POPULATION_CODES),
                'genotype':     widgets.field.Combobox('genotype', choices=genotype['records']),
                'risk':         widgets.field.Textarea('risk'),
                'odd_ratio':    widgets.field.Textbox('odd_ratio'),
                'evidences':    widgets.field.Textarea('evidences'),
                'pmid':         widgets.field.Textbox('pmid')
            }))
            form.renderer.add_section('Variation - Effect')
            form.renderer.add_field('risks', 'Risks', columns=[
                {'id': 'popcode',     'label': 'Popcode',   'width': '10%'},
                {'id': 'genotype',    'label': 'Genotype',  'width': '10%'},
                {'id': 'risk',        'label': 'Risk',      'width': '25%'},
                {'id': 'odd_ratio',   'label': 'Odd ratio', 'width': '10%'},
                {'id': 'evidences',   'label': 'Evidences', 'width': '25%'},
                {'id': 'pmid',        'label': 'PMID',      'width': '10%'},
            ])
        if kind == 'general_alias':
            form.add_field(widgets.field.List('alias', {
                'alias':     widgets.field.Textbox('alias')
            }))
            form.renderer.add_section('General - Alias')
            form.renderer.add_field('alias', 'Alias', columns=[
                {'id': 'alias',        'label': 'ALIAS',       'width': '50%'}
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
                {'id': 'pubmedid',          'label': 'Pubmedid',    'width': '20%'},
                {'id': 'title',             'label': 'Title',       'width': '30%'},
                {'id': 'sentence',          'label': 'Sentence',    'width': '30%'},
            ])
        if kind == 'variation_infobox':
            form.add_field(widgets.field.List('infobox', {
                'key':     widgets.field.Textbox('key'),
                'value':      widgets.field.Textbox('value')
            }))
            form.renderer.add_section('Variation - Infobox')
            form.renderer.add_field('infobox', 'Infobox', columns=[
                {'id': 'key',        'label': 'KEY',       'width': '40%'},
                {'id': 'value',      'label': 'VALUE',     'width': '40%'}
            ])
        if kind == 'variation_frequency':
            form.add_field(widgets.field.List('frequencies', {
                'popcode':              widgets.field.Combobox('popcode', choices=constants.POPULATION_CODES),
                'genotype_count_00':    widgets.field.Textbox('genotype_count_00'),
                'genotype_count_01':    widgets.field.Textbox('genotype_count_01'),
                'genotype_count_11':    widgets.field.Textbox('genotype_count_11'),
            }))
            form.renderer.add_section('Variation - Frequency')
            form.renderer.add_field('frequencies', 'Frequencies', columns=[
                {'id': 'popcode',              'label': 'POPCODE',              'width': '20%'},
                {'id': 'genotype_count_00',     'label': 'Genotype_count_00',   'width': '20%'},
                {'id': 'genotype_count_01',     'label': 'Genotype_count_01',   'width': '20%'},
                {'id': 'genotype_count_11',     'label': 'Genotype_count_11',   'width': '20%'}
            ])

        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        form.renderer.set_field_renderer('list', renderers.widgets.field.ListRenderer())
        return form
    def load_form(self, form):
        result = components.VariationBlockStore(self.get_container()).get(self.params['id'])
        if result['status'] == 'ok':
            record = result['data']['record']
            form.set_form_data(record)
        else:
            form.add_message('danger', "Can't load form")
    def process_form_data(self, data):
        return components.VariationBlockStore(self.get_container()).update(data, self.params['id'])


class Delete(actions.crud.DeleteAction):
    def GET(self):
        result = components.VariationBlockStore(self.get_container()).delete(self.params['id'])
        return HttpResponseRedirect('/variation/detail/%s/block/list' % self.params['variation_id'])
