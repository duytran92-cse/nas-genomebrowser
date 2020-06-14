from django.template import loader
from notasquare.urad_web.renderers import BaseRenderer
import math
import string

class ListRenderer(BaseRenderer):
    def __init__(self):
        super(ListRenderer, self).__init__()
        self.template = 'genopedia/treatment/list.html'
    def render(self, table):
        template = loader.get_template(self.template)
        # Cal
        total_pages = int(math.ceil(table.data['total_matched'] * 1.0 / 60))
        start_index = max(1, table.data['current_page'] - 2)
        end_index = min(total_pages, table.data['current_page'] + 2 ) + 1
        # Data
        context = {}
        context['total_matched'] = table.data['total_matched']
        context['records'] = table.data['records']
        context['current_page'] = table.data['current_page']
        context['previous_page'] = int(table.data['current_page']) - 1
        context['next_page'] = int(table.data['current_page']) + 1
        # Paging
        context['pages_range'] = range(start_index, end_index)
        context['total_pages'] = total_pages
        # Letter
        context['alphabet'] = string.lowercase[:26]
        context['current_letter'] = table.data['current_letter']

        return template.render(context)
