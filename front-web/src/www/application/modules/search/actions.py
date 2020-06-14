from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from notasquare.urad_web import actions, page_contexts, widgets
from application.modules.common import page_contexts, actions as common_actions, components as common_components
from notasquare.urad_web.renderers import BaseRenderer
from django.template import loader
from application import constants
from . import components

class Search(common_actions.BaseAction):
    class SearchRenderer(BaseRenderer):
        def render(self, table):
            if table.data['count'] == 0:
                template = loader.get_template('genopedia/search/404_search_result.html')
            else:
                template = loader.get_template('genopedia/search/search.html')
            context = {}
            context['keyword'] = table.data['keyword']
            context['searchResult'] = table.data['matches']
            context['countResult'] = table.data['count']
            return template.render(context)
    def create_table(self):
        table = widgets.table.DataTable()
        table.renderer = self.SearchRenderer()
        return table
    def load_table_data(self):
        return components.SearchStore(self.get_container()).search(self.params['kw'])
    def GET(self):
        if self.params['kw'] == '':
            return HttpResponseRedirect('/')
        page_context = self.create_page_context()
        table_widget = self.create_table()
        data = self.load_table_data()
        count = 0
        for key, value in data['matches'].items():
            count = count + len(value)
        if count == 1:
            for key, value in data['matches'].items():
                for i in value:
                    if i['name'].lower() == self.params['kw'].lower():
                        if i['reference'] == '':
                            # Redirect link to product
                            return HttpResponseRedirect('/%s/%s' % (key, i['name']))
        # End if count == 1 then redirect to product
        data['keyword'] = self.params['kw']
        data['count'] = count
        table_widget.set_data(data)
        page_context.add_widget(table_widget)
        return HttpResponse(page_context.render())
