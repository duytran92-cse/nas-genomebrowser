from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from notasquare.urad_web import actions, page_contexts, widgets
from notasquare.urad_web_material import renderers
from application import constants
from . import components
from notasquare.urad_web.renderers import BaseRenderer
from django.template import loader

class List(actions.crud.ListAction):
    def create_page_context(self):
        return components.FullPageContext(self.params, self.container)
    class TableRenderer(renderers.widgets.table.DataTableRenderer):
        def render_cell_actions(self, table, row):
            html  = '<div class="btn-group btn-group">'
            html += '<a class="btn btn-xs btn-primary" href="/page/update/%s">Edit</a>' % (row['id'])
            html += '<a class="btn btn-xs btn-danger" href="/page/delete/%s" onclick="return confirm(\'Are you really want to delete this?\')">Delete</a>'  % (row['id'])
            html += '</div>'
            return html
    def create_table(self):
        table = widgets.table.DataTable()
        table.set_title('Page')
        table.set_subtitle('List of pages')
        table.create_button('create', '/page/create', 'zmdi-plus')
        table.create_column('id', 'ID', '8%', sortable=True)
        table.create_column('title', 'Title', '60%')
        table.create_column('actions', '', '14%')
        table.add_field(widgets.field.Textbox('text'))
        table.renderer = self.TableRenderer()
        table.renderer.table_form_renderer = renderers.widgets.form.TableFormRenderer()
        table.renderer.table_form_renderer.add_field('text', 'Text', colspan=8)
        table.renderer.table_form_renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        return table
    def load_table_data(self, table_form_data, sortkey, sortdir, page_number):
        return components.PageStore(self.get_container()).list(table_form_data, sortkey, sortdir, page_number)


class Create(actions.crud.CreateAction):
    def create_page_context(self):
        return components.FullPageContext(self.params, self.container)
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('Page')
        form.add_field(widgets.field.Textbox('title'))
        form.add_field(widgets.field.Richtext('content'))
        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('Page')
        form.renderer.add_field('title', 'Title')
        form.renderer.add_field('content', 'Content', rows=15)
        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('richtext', renderers.widgets.field.RichtextRenderer())
        return form
    def load_form(self, form):
        form.set_form_data({
        })
    def process_form_data(self, data):
        return components.PageStore(self.get_container()).create(data)


class Update(actions.crud.UpdateAction):
    def create_page_context(self):
        return components.FullPageContext(self.params, self.container)
    def create_form(self):
        page_block = components.PageStore(self.get_container()).get(self.params['page_id'])
        form = widgets.form.Form()
        form.set_title('Page')
        form.add_field(widgets.field.Textbox('title'))
        form.add_field(widgets.field.Richtext('content'))
        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('Page')
        form.renderer.add_field('title', 'Title')
        form.renderer.add_field('content', 'Content', rows=15)

        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('richtext', renderers.widgets.field.RichtextRenderer())
        return form

    def load_form(self, form):
        result = components.PageStore(self.get_container()).get(self.params['page_id'])
        if result['status'] == 'ok':
            record = result['data']['record']
            form.set_form_data(record)
        else:
            form.add_message('danger', "Can't load form")
    def process_form_data(self, data):
        return components.PageStore(self.get_container()).update(data, self.params['page_id'])


class Delete(actions.crud.DeleteAction):
    def GET(self):
        result = components.PageStore(self.get_container()).delete(self.params['id'])
        return HttpResponseRedirect('/page/list')

class Validation(actions.crud.FormAction):
    def create_page_context(self):
        return components.FullPageContext(self.params, self.container)
    class ValidationPageRenderer(BaseRenderer):
        def render(self, table):
            template = loader.get_template('material/dashboard/validation.html')
            context = {}
            context['unstable'] = table.data['records']
            context['stable'] = table.data['stable']
            return template.render(context)
    def create_table(self):
        table = widgets.table.DataTable()
        table.renderer = self.ValidationPageRenderer()
        return table
    def load_table_data(self):
        return components.PageStore(self.get_container()).list_blocks()
    def GET(self):
        page_context = self.create_page_context()
        table_widget = self.create_table()
        data = self.load_table_data()
        data = data['record']
        table_widget.set_data(data)
        page_context.add_widget(table_widget)
        return HttpResponse(page_context.render())

class ValidationVariation(actions.crud.FormAction):
    def create_page_context(self):
        return components.FullPageContext(self.params, self.container)
    class VariationPageRenderer(BaseRenderer):
        def render(self, table):
            template = loader.get_template('material/dashboard/validation.html')
            context = {}
            context['unstable'] = table.data['records']
            context['stable'] = table.data['stable']
            return template.render(context)
    def create_table(self):
        table = widgets.table.DataTable()
        table.renderer = self.VariationPageRenderer()
        return table
    def load_table_data(self):
        return components.PageStore(self.get_container()).get_blocks_variation(self.params['id'])
    def GET(self):
        page_context = self.create_page_context()
        table_widget = self.create_table()
        data = self.load_table_data()
        data = data['record']
        table_widget.set_data(data)
        page_context.add_widget(table_widget)
        return HttpResponse(page_context.render())

class ValidationDisease(actions.crud.FormAction):
    def create_page_context(self):
        return components.FullPageContext(self.params, self.container)
    class DiseasePageRenderer(BaseRenderer):
        def render(self, table):
            template = loader.get_template('material/dashboard/validation.html')
            context = {}
            context['unstable'] = table.data['records']
            context['stable'] = table.data['stable']
            return template.render(context)
    def create_table(self):
        table = widgets.table.DataTable()
        table.renderer = self.DiseasePageRenderer()
        return table
    def load_table_data(self):
        return components.PageStore(self.get_container()).get_blocks_disease(self.params['id'])
    def GET(self):
        page_context = self.create_page_context()
        table_widget = self.create_table()
        data = self.load_table_data()
        data = data['record']
        table_widget.set_data(data)
        page_context.add_widget(table_widget)
        return HttpResponse(page_context.render())

class ValidationGene(actions.crud.FormAction):
    def create_page_context(self):
        return components.FullPageContext(self.params, self.container)
    class GenePageRenderer(BaseRenderer):
        def render(self, table):
            template = loader.get_template('material/dashboard/validation.html')
            context = {}
            context['unstable'] = table.data['records']
            context['stable'] = table.data['stable']
            return template.render(context)
    def create_table(self):
        table = widgets.table.DataTable()
        table.renderer = self.GenePageRenderer()
        return table
    def load_table_data(self):
        return components.PageStore(self.get_container()).get_blocks_gene(self.params['id'])
    def GET(self):
        page_context = self.create_page_context()
        table_widget = self.create_table()
        data = self.load_table_data()
        data = data['record']
        table_widget.set_data(data)
        page_context.add_widget(table_widget)
        return HttpResponse(page_context.render())

class ValidationTrait(actions.crud.FormAction):
    def create_page_context(self):
        return components.FullPageContext(self.params, self.container)
    class TraitPageRenderer(BaseRenderer):
        def render(self, table):
            template = loader.get_template('material/dashboard/validation.html')
            context = {}
            context['unstable'] = table.data['records']
            context['stable'] = table.data['stable']
            return template.render(context)
    def create_table(self):
        table = widgets.table.DataTable()
        table.renderer = self.TraitPageRenderer()
        return table
    def load_table_data(self):
        return components.PageStore(self.get_container()).get_blocks_trait(self.params['id'])
    def GET(self):
        page_context = self.create_page_context()
        table_widget = self.create_table()
        data = self.load_table_data()
        data = data['record']
        table_widget.set_data(data)
        page_context.add_widget(table_widget)
        return HttpResponse(page_context.render())

class ValidationTreatment(actions.crud.FormAction):
    def create_page_context(self):
        return components.FullPageContext(self.params, self.container)
    class TreatmentPageRenderer(BaseRenderer):
        def render(self, table):
            template = loader.get_template('material/dashboard/validation.html')
            context = {}
            context['unstable'] = table.data['records']
            context['stable'] = table.data['stable']
            return template.render(context)
    def create_table(self):
        table = widgets.table.DataTable()
        table.renderer = self.TreatmentPageRenderer()
        return table
    def load_table_data(self):
        return components.PageStore(self.get_container()).get_blocks_treatment(self.params['id'])
    def GET(self):
        page_context = self.create_page_context()
        table_widget = self.create_table()
        data = self.load_table_data()
        data = data['record']
        table_widget.set_data(data)
        page_context.add_widget(table_widget)
        return HttpResponse(page_context.render())

class BlockApprove(actions.crud.DeleteAction):
    def GET(self):
        # Update is_stable = True in database
        self.params['version_status'] = 'active'
        result = components.PageStore(self.get_container()).block_stable_update(self.params)
        return HttpResponseRedirect('/page/validation')

class BlockReject(actions.crud.DeleteAction):
    def GET(self):
        # Update is_stable = True in database
        self.params['version_status'] = 'rejected'
        result = components.PageStore(self.get_container()).block_stable_update(self.params)
        return HttpResponseRedirect('/page/validation')
