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
            html += '<a class="btn btn-xs btn-primary" href="/variation/detail/%s/block/detail/%s/pub_text_version/update/%s">Edit</a>' % (row['variation'], row['variation_block'], row['id'])
            html += '<a class="btn btn-xs btn-danger" href="/variation/detail/%s/block/detail/%s/pub_text_version/delete/%s" onclick="return confirm(\'Are you really want to delete this?\')">Delete</a>'  % (row['variation'], row['variation_block'], row['id'])
            html += '<a class="btn btn-xs btn-info" href="/variation/detail/%s/block/detail/%s/pub_text_version/active/%s">Active</a>'  % (row['variation'], row['variation_block'], row['id'])
            html += '</div>'
            return html
    def create_table(self):
        table = widgets.table.DataTable()
        table.set_title('Block Versions')
        table.set_subtitle('List of variation block publication text versions')
        table.create_column('version', 'Version', '10%', sortable=True)
        table.create_column('version_status', 'Status', '10%', sortable=True)
        table.create_column('title', 'Title', '18%', sortable=True)
        table.create_column('text', 'Text', '24%')
        table.create_column('author', 'Author', '10%')
        table.create_column('verify', 'Verify', '10%')
        table.create_column('actions', '', '18%')
        table.add_field(widgets.field.Textbox('text'))
        table.renderer = self.TableRenderer()
        table.renderer.table_form_renderer = renderers.widgets.form.TableFormRenderer()
        table.renderer.table_form_renderer.add_field('text', 'Text', colspan=12)
        table.renderer.table_form_renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        return table
    def load_table_data(self, table_form_data, sortkey, sortdir, page_number):
        table_form_data['variation_block_id'] = self.params['variation_block_id']
        table_form_data['variation_id'] = self.params['variation_id']
        return components.VariationBlockPublicationTextVersionStore(self.get_container()).list(table_form_data, sortkey, sortdir, page_number)

class Update(actions.crud.UpdateAction):
    def create_page_context(self):
        return components.FullPageContext(self.params, self.container)
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('Variation block versions')
        form.add_field(widgets.field.Textbox('version'))
        form.add_field(widgets.field.Combobox('version_status', choices=constants.PAGE_BLOCK_VERSION_STATUS))
        form.add_field(widgets.field.Textbox('created_at'))
        form.add_field(widgets.field.Textbox('title'))
        form.add_field(widgets.field.Textarea('sentence'))
        form.add_field(widgets.field.Textbox('author'))

        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('Variation block versions')
        form.renderer.add_field('version', 'Version')
        form.renderer.add_field('version_status', 'Status')
        form.renderer.add_field('created_at', 'Created_at')
        form.renderer.add_field('title', 'Title')
        form.renderer.add_field('sentence', 'Sentence', rows=15)
        form.renderer.add_field('author', 'Author')

        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        form.renderer.set_field_renderer('list', renderers.widgets.field.ListRenderer())
        return form
    def load_form(self, form):
        result = components.VariationBlockPublicationTextVersionStore(self.get_container()).get(self.params['text_id'])
        if result['status'] == 'ok':
            record = result['data']['record']
            form.set_form_data(record)
        else:
            form.add_message('danger', "Can't load form")
    def process_form_data(self, data):
        return components.VariationBlockPublicationTextVersionStore(self.get_container()).update(data, self.params['text_id'])


class Delete(actions.crud.DeleteAction):
    def GET(self):
        result = components.VariationBlockPublicationTextVersionStore(self.get_container()).delete(self.params['text_id'])
        return HttpResponseRedirect('/variation/detail/%s/block/detail/%s/pub_text_version/list' % (self.params['variation_id'], self.params['variation_block_id']))

class Active(actions.crud.DeleteAction):
    def GET(self):
        result = components.VariationBlockPublicationTextVersionStore(self.get_container()).active(self.params['text_id'])
        return HttpResponseRedirect('/variation/detail/%s/block/detail/%s/pub_text_version/list' % (self.params['variation_id'], self.params['variation_block_id']))

class ActiveSum(actions.crud.DeleteAction):
    def GET(self):
        result = components.VariationBlockPublicationTextVersionStore(self.get_container()).active(self.params['text_id'])
        return HttpResponseRedirect('/variation/summary/%s' % (self.params['pub_text_version']))
