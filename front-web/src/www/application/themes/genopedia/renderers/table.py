from django.template import loader
from notasquare.urad_web.renderers import BaseRenderer

class ListRenderer(BaseRenderer):
    def __init__(self):
        super(ListRenderer, self).__init__()
        self.template = 'genopedia/table/list.html'
    def render_row(self, table, row):
        return '<li><a href="">' + row['rsnumber'] + '</a></li>'
    def render(self, table):
        template = loader.get_template(self.template)
        context = {}
        context['title'] = table.title
        context['subtitle'] = table.subtitle

        rows_html = ''
        for row in table.data:
            rows_html += self.render_row(table, row)
        context['rows_html'] = rows_html

        return template.render(context)
