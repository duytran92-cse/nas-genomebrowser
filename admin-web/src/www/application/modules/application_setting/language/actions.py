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
            html += '<a class="btn btn-xs btn-primary" href="/language/update/%s">Edit</a>' % (row['id'])
            html += '<a class="btn btn-xs btn-danger" href="/language/delete/%s" onclick="return confirm(\'Are you really want to delete this?\')">Delete</a>'  % (row['id'])
            html += '</div>'
            return html
    def create_table(self):
        table = widgets.table.DataTable()
        table.set_title('Language')
        table.set_subtitle('List of languages')
        table.create_button('create', '/language/create', 'zmdi-plus')
        table.create_column('id', 'ID', '10%', sortable=True)
        table.create_column('title', 'Title', '50%')
        table.create_column('code', 'Code', '20%')
        table.create_column('actions', '', '20%')
        table.add_field(widgets.field.Textbox('title'))
        table.add_field(widgets.field.Textbox('code'))
        table.renderer = self.TableRenderer()
        table.renderer.table_form_renderer = renderers.widgets.form.TableFormRenderer()
        table.renderer.table_form_renderer.add_field('title', 'Title', colspan=4)
        table.renderer.table_form_renderer.add_field('code', 'Code', colspan=4)
        table.renderer.table_form_renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        return table
    def load_table_data(self, table_form_data, sortkey, sortdir, page_number):
        return components.LanguageStore(self.get_container()).list(table_form_data, sortkey, sortdir, page_number)

class Create(actions.crud.CreateAction):
    def create_page_context(self):
        return components.FullPageContext(self.params, self.container)
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('Language')
        form.add_field(widgets.field.Textbox('title'))
        form.add_field(widgets.field.Textbox('code'))
        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('Create new language')
        form.renderer.add_field('title', 'Title')
        form.renderer.add_field('code', 'Code')
        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        return form
    def load_form(self, form):
        form.set_form_data({
        })
    def process_form_data(self, data):
        return components.LanguageStore(self.get_container()).create(data)


class Update(actions.crud.UpdateAction):
    def create_page_context(self):
        return components.FullPageContext(self.params, self.container)
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('Language')
        form.add_field(widgets.field.Textbox('title'))
        form.add_field(widgets.field.Textbox('code'))

        form.renderer = renderers.widgets.form.HorizontalFormRenderer()

        form.renderer.add_section('Update language')
        form.renderer.add_field('title', 'Title')
        form.renderer.add_field('code', 'Code')

        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        return form

    def load_form(self, form):
        result = components.LanguageStore(self.get_container()).get(self.params['language_id'])
        if result['status'] == 'ok':
            record = result['data']['record']
            form.set_form_data(record)
        else:
            form.add_message('danger', "Can't load form")
    def process_form_data(self, data):
        return components.LanguageStore(self.get_container()).update(data, self.params['language_id'])

class Delete(actions.crud.DeleteAction):
    def GET(self):
        result = components.LanguageStore(self.get_container()).delete(self.params['id'])
        return HttpResponseRedirect('/language/list')
