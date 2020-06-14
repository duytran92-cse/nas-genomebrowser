from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from notasquare.urad_web import actions, page_contexts, widgets
from notasquare.urad_web_material import renderers
from application import constants
from . import components
from application.modules.application_setting.language import components as lang_components

class List(actions.crud.ListAction):
    def create_page_context(self):
        return components.FullPageContext(self.params, self.container)
    class TableRenderer(renderers.widgets.table.DataTableRenderer):
        def render_cell_actions(self, table, row):
            html  = '<div class="btn-group btn-group">'
            html += '<a class="btn btn-xs btn-primary" href="/text_block/update/%s">Edit</a>' % (row['id'])
            html += '<a class="btn btn-xs btn-danger" href="/text_block/delete/%s" onclick="return confirm(\'Are you really want to delete this?\')">Delete</a>'  % (row['id'])
            html += '</div>'
            return html
    def create_table(self):
        table = widgets.table.DataTable()
        table.set_title('Text Block')
        table.set_subtitle('List of text blocks')
        table.create_button('create', '/text_block/create', 'zmdi-plus')
        table.create_column('id', 'ID', '10%', sortable=True)
        table.create_column('text', 'Text', '60%')
        table.create_column('kind', 'Kind', '15%')
        table.create_column('actions', '', '14%')
        table.add_field(widgets.field.Textbox('text'))
        table.renderer = self.TableRenderer()
        table.renderer.table_form_renderer = renderers.widgets.form.TableFormRenderer()
        table.renderer.table_form_renderer.add_field('text', 'Text', colspan=8)
        table.renderer.table_form_renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        return table
    def load_table_data(self, table_form_data, sortkey, sortdir, page_number):
        return components.TextBlockStore(self.get_container()).list(table_form_data, sortkey, sortdir, page_number)

class Create(actions.crud.CreateAction):
    def create_page_context(self):
        return components.FullPageContext(self.params, self.container)
    def create_form(self):
        language = lang_components.LanguageStore(self.get_container()).populate_combobox()
        form = widgets.form.Form()
        form.set_title('Text Block')
        form.add_field(widgets.field.Textarea('text'))
        form.add_field(widgets.field.Combobox('kind', choices=constants.TEXTBLOCK_KINDS))
        form.add_field(widgets.field.List('translation', {
            'language':         widgets.field.Combobox('language', choices=language),
            'translate':        widgets.field.Textarea('translate')
        }))
        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('Create new text block')
        form.renderer.add_field('text', 'Text', rows=10)
        form.renderer.add_field('kind', 'Kind')
        form.renderer.add_field('translation', 'Translation', columns=[
            {'id': 'language',      'label': 'Language',         'width': '20%'},
            {'id': 'translate',     'label': 'Translate',        'width': '70%'}
        ])
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        form.renderer.set_field_renderer('list', renderers.widgets.field.ListRenderer())
        return form
    def load_form(self, form):
        form.set_form_data({
        })
    def process_form_data(self, data):
        return components.TextBlockStore(self.get_container()).create(data)


class Update(actions.crud.UpdateAction):
    def create_page_context(self):
        return components.FullPageContext(self.params, self.container)
    def create_form(self):
        language = lang_components.LanguageStore(self.get_container()).populate_combobox()
        form = widgets.form.Form()
        form.set_title('Text Block')
        form.add_field(widgets.field.Textarea('text'))
        form.add_field(widgets.field.Combobox('kind', choices=constants.TEXTBLOCK_KINDS))
        form.add_field(widgets.field.List('translation', {
            'language':         widgets.field.Combobox('language', choices=language),
            'translate':        widgets.field.Textarea('translate'),
        }))
        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('Update text block')
        form.renderer.add_field('text', 'Text', rows=10)
        form.renderer.add_field('kind', 'Kind')
        form.renderer.add_field('translation', 'Translation', columns=[
            {'id': 'language',          'label': 'Language',        'width': '20%'},
            {'id': 'translate',         'label': 'Translate',       'width': '70%'}
        ])
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        form.renderer.set_field_renderer('list', renderers.widgets.field.ListRenderer())
        return form

    def load_form(self, form):
        result = components.TextBlockStore(self.get_container()).get(self.params['text_block_id'])
        if result['status'] == 'ok':
            record = result['data']['record']
            form.set_form_data(record)
        else:
            form.add_message('danger', "Can't load form")
    def process_form_data(self, data):
        return components.TextBlockStore(self.get_container()).update(data, self.params['text_block_id'])

class Delete(actions.crud.DeleteAction):
    def GET(self):
        result = components.TextBlockStore(self.get_container()).delete(self.params['id'])
        return HttpResponseRedirect('/text_block/list')
