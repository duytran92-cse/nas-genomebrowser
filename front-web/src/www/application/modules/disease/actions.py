from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from notasquare.urad_web import actions, page_contexts, widgets, renderers
from application.modules.common import page_contexts, actions as common_actions, components as common_components
from application.themes.genopedia import renderers as genopedia_renderers
from application.themes.genopedia import widgets as genopedia_widgets
from application import constants
from . import components

class List(common_actions.BaseAction):
    class ListRenderer(genopedia_renderers.disease.ListRenderer):
        pass
    def create_table(self):
        table = widgets.table.DataTable()
        table.renderer = self.ListRenderer()
        return table
    def load_table_data(self, page_number=2, letter='a'):
        return components.DiseaseStore(self.get_container()).list(page_number=page_number, letter=letter)
    def GET(self):
        page_number = int(self.params['page']) if 'page' in self.params else 1
        letter = str(self.params['lt']) if 'lt' in self.params else 'all'
        page_context = self.create_page_context()
        table_widget = self.create_table()
        data = self.load_table_data(page_number, letter)
        table_widget.set_data(data)
        page_context.add_widget(table_widget)
        data['current_page'] = page_number
        data['current_letter'] = letter
        return HttpResponse(page_context.render())


class View(common_actions.BaseAction):
    def create_page_widget(self, page_id):
        page_widget = genopedia_widgets.page.PageWidget()
        page_widget.renderer = genopedia_renderers.page.PageRenderer()
        page = components.DiseaseStore(self.get_container()).get(page_id['disease_name'])
        if page['status'] == 'ok':
            page = page['data']['record']
            for position in page['blocks']:
                for block in page['blocks'][position]:
                    block['key'] = 'disease'
                    page_widget.add_block(position, block)
            page_widget.add_params_page('disease')
            page_widget.add_params_entity(page_id['disease_name'])
        return page_widget
    def GET(self):
        page_context = self.create_page_context()
        page_widget = self.create_page_widget(self.params)
        page_context.add_widget(page_widget)
        return HttpResponse(page_context.render())
