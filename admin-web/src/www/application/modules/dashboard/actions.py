from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from notasquare.urad_web import actions, page_contexts, widgets
from notasquare.urad_web_material import renderers
from application import constants
from . import components

class Dashboard(actions.crud.FormAction):
    def create_page_context(self):
        return components.FullPageContext(self.params, self.container)
    class DashboardRenderer(renderers.dashboard.DashboardRenderer):
        pass
    def create_table(self):
        table = widgets.table.DataTable()
        table.renderer = self.DashboardRenderer()
        return table
    def load_table_data(self):
        return components.DashboardStore(self.get_container()).list()
    def GET(self):
        page_context = self.create_page_context()
        table_widget = self.create_table()
        data = self.load_table_data()
        table_widget.set_data(data['record'])
        page_context.add_widget(table_widget)
        return HttpResponse(page_context.render())
