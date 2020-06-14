from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from notasquare.urad_web import actions, page_contexts, widgets
from notasquare.urad_web_material import renderers
from application import constants
from . import components

class List(actions.crud.ListAction):
    def create_page_context(self):
        return components.FullPageContext(self.params, self.container)
    class TableRenderer(renderers.widgets.table.DataTableRenderer):
        def render_cell_actions(self, table, row):
            html  = '<div class="btn-group btn-group">'
            html += '    <a class="btn btn-xs btn-primary" href="/disease/detail/%s/block/detail/%s/pub_version/update/%s">Edit</a>' % (row['disease'], row['disease_block'], row['id'])
            html += '    <a class="btn btn-xs btn-danger" href="/disease/detail/%s/block/detail/%s/pub_version/delete/%s" onclick="return confirm(\'Are you really want to delete this?\')">Delete</a>'  % (row['disease'], row['disease_block'], row['id'])
            html += '    <a class="btn btn-xs btn-info" href="/disease/detail/%s/block/detail/%s/pub_version/active/%s">Active</a>'  % (row['disease'], row['disease_block'], row['id'])
            html += '</div>'
            return html
    def create_table(self):
        table = widgets.table.DataTable()
        table.set_title('Block Versions')
        table.set_subtitle('List of disease block versions')
        table.create_column('id', 'Version', '8%', sortable=True)
        table.create_column('version_status', 'Status', '8%', sortable=True)
        table.create_column('created_at', 'Timestamp', '10%', sortable=True)
        table.create_column('author', 'Author', '20%')
        table.create_column('verify', 'Verify', '20%')
        table.create_column('actions', '', '20%')
        table.add_field(widgets.field.Textbox('text'))
        table.renderer = self.TableRenderer()
        table.renderer.table_form_renderer = renderers.widgets.form.TableFormRenderer()
        table.renderer.table_form_renderer.add_field('text', 'Text', colspan=12)
        table.renderer.table_form_renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        return table
    def load_table_data(self, table_form_data, sortkey, sortdir, page_number):
        table_form_data['disease_block_id'] = self.params['disease_block_id']
        table_form_data['disease_id'] = self.params['disease_id']
        return components.DiseaseBlockPublicationVersionStore(self.get_container()).list(table_form_data, sortkey, sortdir, page_number)

class Update(actions.crud.UpdateAction):
    def create_page_context(self):
        return components.FullPageContext(self.params, self.container)
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('Disease block publication versions')
        form.add_field(widgets.field.Textbox('version'))
        form.add_field(widgets.field.Combobox('version_status', choices=constants.PAGE_BLOCK_VERSION_STATUS))
        form.add_field(widgets.field.Textbox('created_at'))
        form.add_field(widgets.field.Textbox('author'))

        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('Disease block versions')
        form.renderer.add_field('version', 'Version')
        form.renderer.add_field('version_status', 'Status')
        form.renderer.add_field('created_at','Timestamp')
        form.renderer.add_field('author', 'Author')

        # Show publication
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

        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        form.renderer.set_field_renderer('list', renderers.widgets.field.ListRenderer())
        return form
    def load_form(self, form):
        result = components.DiseaseBlockPublicationVersionStore(self.get_container()).get(self.params['pub_id'])
        if result['status'] == 'ok':
            record = result['data']['record']
            form.set_form_data(record)
        else:
            form.add_message('danger', "Can't load form")
    def process_form_data(self, data):
        return components.DiseaseBlockPublicationVersionStore(self.get_container()).update(data, self.params['pub_id'])


class Delete(actions.crud.DeleteAction):
    def GET(self):
        result = components.DiseaseBlockPublicationVersionStore(self.get_container()).delete(self.params['pub_id'])
        return HttpResponseRedirect('/disease/detail/%s/block/detail/%s/pub_version/list' % (self.params['disease_id'], self.params['disease_block_id']))

class Active(actions.crud.DeleteAction):
    def GET(self):
        result = components.DiseaseBlockPublicationVersionStore(self.get_container()).active(self.params['text_id'])
        return HttpResponseRedirect('/disease/detail/%s/block/detail/%s/pub_version/list' % (self.params['disease_id'], self.params['disease_block_id']))

class ActiveSum(actions.crud.DeleteAction):
    def GET(self):
        result = components.DiseaseBlockPublicationVersionStore(self.get_container()).active(self.params['text_id'])
        return HttpResponseRedirect('/disease/summary/%s' % (self.params['disease_id']))
