from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from notasquare.urad_web import actions, page_contexts, widgets
from notasquare.urad_web_material import renderers
from application import constants
from application.modules.disease import components as disease_components
from application.modules.common import components

class List(actions.crud.ListAction):
    def create_page_context(self):
        return disease_components.FullPageContext(self.params, self.container)
    class TableRenderer(renderers.widgets.table.DataTableRenderer):
        def render_cell_actions(self, table, row):
            html  = '<div class="btn-group btn-group">'
            html += '    <a class="btn btn-xs btn-primary" href="/disease/detail/%s/comment/update/%s">Edit</a>' % (row['page_id'], row['id'])
            html += '    <a class="btn btn-xs btn-danger" href="/disease/detail/%s/comment/delete/%s" onclick="return confirm(\'Are you really want to delete this?\')">Delete</a>'  % (row['page_id'], row['id'])
            html += '</div>'
            return html
    def create_table(self):
        table = widgets.table.DataTable()
        table.set_title('Comments')
        table.set_subtitle('List of disease comments')
        table.create_button('create', '/disease/detail/%s/comment/create' % (self.params['disease_id']), 'zmdi-plus')
        table.create_column('id', 'ID', '8%', sortable=True)
        table.create_column('timestamp', 'Timestamp', '15%', sortable=True)
        table.create_column('user', 'User', '15%')
        table.create_column('comment', 'Comment', '50%')
        table.create_column('actions', '', '14%')
        table.add_field(widgets.field.Textbox('text'))
        table.renderer = self.TableRenderer()
        table.renderer.table_form_renderer = renderers.widgets.form.TableFormRenderer()
        table.renderer.table_form_renderer.add_field('text', 'Text', colspan=12)
        table.renderer.table_form_renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        return table
    def load_table_data(self, table_form_data, sortkey, sortdir, page_number):
        table_form_data['disease_id'] = self.params['disease_id']
        table_form_data['idPage'] = 'disease'
        return components.CommentStore(self.get_container()).list(table_form_data, sortkey, sortdir, page_number)


class Create(actions.crud.CreateAction):
    def create_page_context(self):
        return disease_components.FullPageContext(self.params, self.container)
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('Comment')
        form.add_field(widgets.field.Textbox('user'))
        form.add_field(widgets.field.Textarea('comment'))
        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('Comment')
        form.renderer.add_field('user', 'User')
        form.renderer.add_field('comment', 'Comment', rows=5)
        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        return form
    def load_form(self, form):
        form.set_form_data({
        })
    def process_form_data(self, data):
        data['entity'] = self.params['disease_id']
        data['page'] = 'disease'
        return components.CommentStore(self.get_container()).create(data)


class Update(actions.crud.UpdateAction):
    def create_page_context(self):
        return disease_components.FullPageContext(self.params, self.container)
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('Comment')
        form.add_field(widgets.field.Textbox('user'))
        form.add_field(widgets.field.Textarea('comment'))
        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('Comment')
        form.renderer.add_field('user', 'User')
        form.renderer.add_field('comment', 'Comment', rows=5)
        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        return form
    def load_form(self, form):
        result = components.CommentStore(self.get_container()).get(self.params['id'])
        if result['status'] == 'ok':
            record = result['data']['record']
            form.set_form_data(record)
        else:
            form.add_message('danger', "Can't load form")
    def process_form_data(self, data):
        return components.CommentStore(self.get_container()).update(data, self.params['id'])


class Delete(actions.crud.DeleteAction):
    def GET(self):
        result = components.CommentStore(self.get_container()).delete(self.params['id'])
        return HttpResponseRedirect('/disease/detail/%s/comment/list' % self.params['disease_id'])
