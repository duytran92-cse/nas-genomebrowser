
from notasquare.urad_web.widgets import BaseWidget

class PageWidget(BaseWidget):
    def __init__(self):
        super(PageWidget, self).__init__()
        self.blocks = {
            'main':  [],
            'left':  [],
            'right': []
        }
        self.params = {
            'page': '',
            'entity': ''
        }
    def add_block(self, position, block):
        self.blocks[position].append(block)
    def add_params_page(self, value):
        self.params['page'] = value
    def add_params_entity(self, value):
        self.params['entity'] = value
