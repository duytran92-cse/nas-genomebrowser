from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from notasquare.urad_web import actions, page_contexts, widgets
from notasquare.urad_web_material import renderers
from application import constants
from application.modules.gene import components
from notasquare.urad_web.renderers import BaseRenderer
from django.template import loader

class List(actions.crud.ListAction):
    def create_page_context(self):
        return components.FullPageContext(self.params, self.container)
    class TableRenderer(renderers.widgets.table.DataTableRenderer):
        def render_cell_actions(self, table, row):
            html  = '<div class="btn-group btn-group">'
            html += '<a class="btn btn-xs btn-success" href="%s/gene/%s" target="_blank">View</a>' % (settings.LINK_GENOME_BROWSER_GENOPEDIA,row['title'])
            html += '    <a class="btn btn-xs btn-primary" href="/gene/summary/%s">Edit</a>' % (row['id'])
            html += '    <a class="btn btn-xs btn-danger" href="/gene/delete/%s" onclick="return confirm(\'Are you really want to delete this?\')">Delete</a>'  % (row['id'])
            html += '</div>'
            return html
    def create_table(self):
        table = widgets.table.DataTable()
        table.set_title('Gene')
        table.set_subtitle('List of genes')
        table.create_button('create', '/gene/create', 'zmdi-plus')
        table.create_column('id', 'ID', '10%', sortable=True)
        table.create_column('title', 'Title', '60%')
        table.create_column('actions', '', '14%')
        table.add_field(widgets.field.Textbox('text'))
        table.renderer = self.TableRenderer()
        table.renderer.table_form_renderer = renderers.widgets.form.TableFormRenderer()
        table.renderer.table_form_renderer.add_field('text', 'Text', colspan=8)
        table.renderer.table_form_renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        return table
    def load_table_data(self, table_form_data, sortkey, sortdir, page_number):
        return components.GeneStore(self.get_container()).list(table_form_data, sortkey, sortdir, page_number)

class Create(actions.crud.CreateAction):
    def create_page_context(self):
        return components.FullPageContext(self.params, self.container)
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('Gene')
        form.add_field(widgets.field.Textbox('title'))
        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('Gene')
        form.renderer.add_field('title', 'Title')

        form.add_field(widgets.field.List('associated_diseases', {
            'disease_name':     widgets.field.Textbox('disease_name'),
        }))
        form.renderer.add_field('associated_diseases', 'Associated Diseases', columns=[
            {'id': 'disease_name',        'label': 'Disease',       'width': '90%'},
        ])

        form.add_field(widgets.field.List('associated_publications', {
            'pmid':     widgets.field.Textbox('pmid'),
            'doi':      widgets.field.Textbox('doi'),
            'pmc':      widgets.field.Textbox('pmc'),
            'title':    widgets.field.Textarea('title'),
            'authors':  widgets.field.Textarea('authors'),
            'journal':  widgets.field.Textarea('journal')
        }))

        form.renderer.add_field('associated_publications', 'Associated Publications', columns=[
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
        form.set_form_data({
        })
    def process_form_data(self, data):
        res = components.GeneStore(self.get_container()).create(data)
        self.params['id'] = res['data']['pk']
        return res
    def handle_on_success(self, messages):
        return HttpResponseRedirect('/gene/update/%s' % (self.params["id"]))


class Update(actions.crud.UpdateAction):
    def create_page_context(self):
        context = components.FullPageContext(self.params, self.container)
        context.submenu.set_entry_selected('update')
        return context
    def create_form(self):

        form = widgets.form.Form()
        form.set_title('Gene')
        form.add_field(widgets.field.Textbox('title'))
        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('Gene')
        form.renderer.add_field('title', 'Title')

        form.add_field(widgets.field.List('associated_diseases', {
            'disease_name':     widgets.field.Textbox('disease_name'),
        }))
        form.renderer.add_field('associated_diseases', 'Associated Diseases', columns=[
            {'id': 'disease_name',        'label': 'Disease',       'width': '90%'},
        ])
        
        form.add_field(widgets.field.List('associated_publications', {
            'pmid':     widgets.field.Textbox('pmid'),
            'doi':      widgets.field.Textbox('doi'),
            'pmc':      widgets.field.Textbox('pmc'),
            'title':    widgets.field.Textarea('title'),
            'authors':  widgets.field.Textarea('authors'),
            'journal':  widgets.field.Textarea('journal')
        }))

        form.renderer.add_field('associated_publications', 'Associated Publications', columns=[
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
        result = components.GeneStore(self.get_container()).get(self.params['gene_id'])
        if result['status'] == 'ok':
            record = result['data']['record']
            form.set_form_data(record)
        else:
            form.add_message('danger', "Can't load form")
    def process_form_data(self, data):
        return components.GeneStore(self.get_container()).update(data, self.params['gene_id'])
    def handle_on_success(self, messages):
        self.form = self.create_form()
        for message in messages:
            self.form.add_message(message['type'], message['message'] + ' Click <a href="%s/gene/%s">HERE</a> to view on production' % (settings.LINK_GENOME_BROWSER_GENOPEDIA, self.params['title']))
        self.load_form(self.form)
        self.page_context = self.create_page_context()
        self.page_context.add_widget(self.form)
        return HttpResponse(self.page_context.render())


class Delete(actions.crud.DeleteAction):
    def GET(self):
        result = components.GeneStore(self.get_container()).delete(self.params['id'])
        return HttpResponseRedirect('/gene/list')

class Summary(actions.crud.FormAction):
    def create_page_context(self):
        context = components.FullPageContext(self.params, self.container)
        context.submenu.set_entry_selected('summary')
        return context

    class GeneSummaryRenderer(BaseRenderer):
        def render(self, table):
            template = loader.get_template('material/summary/summary.html')
            context = {}
            context['page_id'] = table.data[0]['gene_id']
            context['page_disease'] = table.data[0]['gene_disease']
            context['title'] = table.data[0]['title']
            context['blocks'] = table.data[0]['blocks']
            context['total_blocks'] = table.data[0]['total_blocks']
            context['total_active_blocks_version'] = table.data[0]['total_active_blocks_version']
            context['active_blocks_version'] = table.data[0]['active_blocks_version']
            context['total_inactive_blocks_version'] = table.data[0]['total_inactive_blocks_version']
            context['inactive_blocks_version'] = table.data[0]['inactive_blocks_version']
            context['total_comments'] = table.data[0]['total_comments']
            context['comments'] = table.data[0]['comments']
            context['link_genome_browser_genopedia'] = settings.LINK_GENOME_BROWSER_GENOPEDIA
            context['page'] = 'gene'
            return template.render(context)
    def create_table(self):
        table = widgets.table.DataTable()
        table.renderer = self.GeneSummaryRenderer()
        return table
    def load_table_data(self):
        return components.GeneStore(self.get_container()).summary(self.params['gene_id'])
    def GET(self):
        page_context = self.create_page_context()
        table_widget = self.create_table()
        data = self.load_table_data()
        data = data['data']['record']
        table_widget.set_data(data)
        page_context.add_widget(table_widget)
        return HttpResponse(page_context.render())
