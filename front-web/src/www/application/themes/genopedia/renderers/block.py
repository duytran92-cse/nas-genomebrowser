from django.template import loader
from notasquare.urad_web.renderers import BaseRenderer

class PageRenderer(BaseRenderer):
    def __init__(self):
        super(PageRenderer, self).__init__()
        self.template = 'genopedia/page/page.html'
    def render_general_text(self, block):
        template = loader.get_template('genopedia/page/editable_block/text_block.html')
        context = {}
        context['id'] = block['id']
        context['title'] = block['title']
        context['text'] = block['text']
        return template.render(context)
    def render_general_publications(self, block):
        template = loader.get_template('genopedia/page/editable_block/publication_block.html')
        context = {}
        context['id'] = block['id']
        context['title'] = block['title']
        context['publications'] = block['publications']
        return template.render(context)
    def render_general_effect(self, block):
        template = loader.get_template('genopedia/page/block/general_effect.html')
        context = {}
        context['title'] = block['title']
        context['risks'] = block['risks']
        context['genotypes'] = block['genotypes']
        return template.render(context)    
    def render_block(self, block):
        if block['kind'] == 'general_text':
            return self.render_general_text(block)
        if block['kind'] == 'general_publications':
            return self.render_general_publications(block)
        if block['kind'] == 'variation_effect':
            return self.render_general_effect(block)
        return '----'
    def render(self, page):
        template = loader.get_template(self.template)
        context = {}
        blocks_html = {}
        for position in page.blocks:
            blocks_html[position] = []
            for block in page.blocks[position]:
                blocks_html[position].append(self.render_block(block))

        context['main_blocks_html'] = blocks_html['main'] if 'main' in blocks_html else []
        context['left_blocks_html'] = blocks_html['left'] if 'left' in blocks_html else []
        context['right_blocks_html'] = blocks_html['right'] if 'right' in blocks_html else []

        return template.render(context)
