from django.template import loader
from notasquare.urad_web.renderers import BaseRenderer
from django.conf import settings
from application import constants
import json
class PageRenderer(BaseRenderer):
    def __init__(self):
        super(PageRenderer, self).__init__()
        self.template = 'genopedia/page/page.html'
    def render_general_text(self, block):
        template = loader.get_template('genopedia/page/block/general_text.html')
        context = {}
        context['id'] = block['id']
        context['title'] = block['title']
        context['text'] = block['text']
        context['key'] = block['key']
        return template.render(context)
    def render_general_publications(self, block):
        template = loader.get_template('genopedia/page/block/general_publications.html')
        context = {}
        context['id'] = block['id']
        context['title'] = block['title']
        context['publications'] = block['publications']
        context['key'] = block['key']
        return template.render(context)
    def render_general_effect(self, block):
        template = loader.get_template('genopedia/page/block/general_effect.html')
        context = {}
        context['id'] = block['id']
        context['title'] = block['title']
        context['genotypes'] = block['genotypes']
        context['risks'] = {}
        context['genotype_js'] = json.dumps(block['genotypes'])
        i = 0
        for risk in block['risks']:
            if block['risks'][i]['genotype'] in context['risks']:
                context['risks'][block['risks'][i]['genotype']].append({
                    'popcode': block['risks'][i]['popcode'],
                    'risk': block['risks'][i]['risk'],
                    'odd_ratio': block['risks'][i]['odd_ratio'],
                    'evidences': block['risks'][i]['evidences'],
                    'pmid': block['risks'][i]['pmid']
                })
            else:
                context['risks'][block['risks'][i]['genotype']] = []
                context['risks'][block['risks'][i]['genotype']].append({
                    'popcode': block['risks'][i]['popcode'],
                    'risk': block['risks'][i]['risk'],
                    'odd_ratio': block['risks'][i]['odd_ratio'],
                    'evidences': block['risks'][i]['evidences'],
                    'pmid': block['risks'][i]['pmid']
                })
            i += 1
        context['key'] = block['key']
        context['pop_active'] = block['filter']
        context['pop'] = constants.POPULATION_CODES_EFFECT
        return template.render(context)
    def render_general_alias(self, block):
        template = loader.get_template('genopedia/page/block/general_alias.html')
        context = {}
        context['id'] = block['id']
        context['title'] = block['title']
        context['alias'] = block['alias']
        context['key'] = block['key']
        return template.render(context)
    def render_general_disgenet_diseases(self, block):
        template = loader.get_template('genopedia/page/block/general_disgenet_diseases.html')
        context = {}
        context['id'] = block['id']
        context['title'] = block['title']
        disgenet_diseases = []
        for r in block['disgenet_diseases']:
            disgenet_diseases.append({
                'disease':          r['title'],
                'pubmedid':         r['pubmedid']
            })
        context['disgenet_show'] = block['disgenet_show']
        context['disgenet_diseases'] = disgenet_diseases
        context['key'] = block['key']
        return template.render(context)
    def render_variation_pub_text(self, block):
        template = loader.get_template('genopedia/page/block/variation_pub_text.html')
        context = {}
        context['id'] = block['id']
        context['title'] = block['title']
        pub_text = []
        for val in block['pub_text']:
            pub_text.append({
                'id':               val['id'],
                'title':            val['title'],
                'pubmedid':         val['pubmedid'],
                'sentence':         val['sentence'].split("\n")
            })
        context['pub_text'] = pub_text
        context['key'] = block['key']
        return template.render(context)
    def render_general_frequency(self, block):
        template = loader.get_template('genopedia/page/block/general_frequency.html')
        context = {}
        context['id'] = block['id']
        context['title'] = block['title']
        context['frequency'] = block['frequencies_front']
        context['key'] = block['key']
        return template.render(context)
    def render_variation_infobox(self, block):
        template = loader.get_template('genopedia/page/block/variation_infobox.html')
        context = {}
        context['id'] = block['id']
        context['title'] = block['title']
        context['infoboxs'] = block['infobox']
        context['key'] = block['key']
        return template.render(context)
    def render_gene_infobox(self, block):
        template = loader.get_template('genopedia/page/block/gene_infobox.html')
        context = {}
        context['id'] = block['id']
        context['title'] = block['title']
        context['infoboxs'] = block['infobox']
        context['key'] = block['key']
        return template.render(context)
    def render_gene_effect(self, block):
        template = loader.get_template('genopedia/page/block/gene_effect.html')
        context = {}
        context['id'] = block['id']
        context['title'] = block['title']
        context['effects'] = block['effects']
        context['key'] = block['key']
        return template.render(context)
    def render_block(self, block):
        if block['kind'] == 'general_text':
            return self.render_general_text(block)
        if block['kind'] == 'general_publications':
            return self.render_general_publications(block)
        if block['kind'] == 'variation_effect':
            return self.render_general_effect(block)
        if block['kind'] == 'general_alias':
            return self.render_general_alias(block)
        if block['kind'] == 'variation_frequency':
            return self.render_general_frequency(block)
        if block['kind'] == 'gene_effect':
            return self.render_gene_effect(block)
        if block['kind'] == 'gene_infobox':
            return self.render_gene_infobox(block)
        if block['kind'] == 'general_disgenet_diseases':
            return self.render_general_disgenet_diseases(block)
        if block['kind'] == 'variation_pub_text':
            return self.render_variation_pub_text(block)
        return '----'
    def render(self, page):
        template = loader.get_template(self.template)
        context = {}
        blocks_html = {}
        info_banner = {}
        for position in page.blocks:
            blocks_html[position] = []
            for block in page.blocks[position]:
                if block['kind'] == 'variation_infobox':
                    for r in block['infobox']:
                        if r['key'] == 'Chromosome':
                            info_banner['chromosome'] = r['value']
                        else:
                            info_banner['genename'] = r['value']

                else:
                    blocks_html[position].append(self.render_block(block))

        context['main_blocks_html'] = blocks_html['main'] if 'main' in blocks_html else []
        context['left_blocks_html'] = blocks_html['left'] if 'left' in blocks_html else []
        context['right_blocks_html'] = blocks_html['right'] if 'right' in blocks_html else []
        if len(context['main_blocks_html']) == 0 and len(context['left_blocks_html']) == 0 and len(context['right_blocks_html']) == 0:
            context['error'] = 'Not found'
        context['entity'] = page.params['entity']
        context['page'] = page.params['page']
        context['info_banner'] = info_banner
        context['lst_chromosome'] = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,'MT','X','Y']
        context['sequence_url'] = settings.NOTASQUARE_SEQUENCE_URL

        return template.render(context)
