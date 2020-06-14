from notasquare.urad_api import *
from application.models import *
from application import constants
from . import components
from django.conf import settings
from django.db.models import Q

class List(handlers.standard.ListHandler):
    def create_query(self, data):
        query = Page.objects
        query = query.filter(is_disabled=False)
        if 'text' in data:
            query = query.filter(title__contains=data['text'])
        if 'kind' in data:
            if data['kind'].strip("\s") != '':
                query = query.filter(kind=data['kind'].strip("\s"))
        return query
    def serialize_entry(self, page):
        return {
            'id':       page.id,
            'title':    page.title
        }

class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        page = Page.objects.get(pk=data['id'])
        return {
            'id': page.id,
            'title': page.title,
            'content': page.content
        }

class Create(handlers.standard.CreateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('title', 'string'):
            self.add_error('title', 'MUST_NOT_BE_EMPTY')
        return parser.get_data()
    def create(self, data):
        page = Page()
        page.title = data['title']
        page.content = data['content']
        page.save()
        return page


class Update(handlers.standard.UpdateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if 'title' in params:
            if not parser.parse('title', 'string'):
                self.add_error('title', 'MUST_NOT_BE_EMPTY')
        return parser.get_data()
    def update(self, data):
        page = Page.objects.get(pk=data['id'])
        if 'title' in data:
            page.title = data['title']
        if 'content' in data:
            page.content = data['content']
        page.save()
        return page


class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        page = Page.objects.get(pk=data['id'])
        page.is_disabled = True
        page.save()
        return 1

class GetContentPage(handlers.standard.GetHandler):
    def get_data(self, data):
        page = Page.objects.get(id=data['page_id'])
        return {
            'content': page.content
        }

class SendMessageContactUs(handlers.standard.FormHandler):
    def POST(self, data):
        # Send email
        contact_us = ContactUs()
        contact_us.email = data['email'],
        contact_us.message = data['message']
        contact_us.save()
        return 1

class GetLangText(handlers.standard.GetHandler):
    def get_data(self, data):
        result = {}
        query = TextBlockLanguage.objects
        if 'lang' in data:
            query = query.filter(language=data['lang'])
        else:
            query = query.filter(language='en')

        for item in query:
            text = TextBlock.objects.get(pk=item.text_block_id)
            result[text.text_code] = item.translate
        return result


class Search(handlers.standard.GetHandler):
    def get_data(self, data):
        result = {}
        keyword = data['kw'].split(' ')
        Qs = []
        for k in keyword:
            Qs.append(Q(name__icontains=k))
        matches = SearchIndex.objects.filter(reduce(lambda x,y: x & y, Qs))

        result = {
            'matches': {
                'variation': [],
                'gene': [],
                'treatment': [],
                'trait': [],
                'disease': [],
                'medications': []
            },
            'num': matches.count()
        }
        if matches:
            for m in matches:
                if m.ctype in result['matches']:
                    result['matches'][m.ctype].append({
                        'name': m.name,
                        'reference':m.reference,
                    })
        return result

class Dashboard(handlers.standard.GetHandler):
    def get_data(self, data):
        data = []
        links = []

        variation_records = Variation.objects.all().count()
        gene_records = Gene.objects.all().count()
        disease_records = Disease.objects.all().count()
        trait_records = Trait.objects.all().count()
        treatment_records = Treatment.objects.all().count()

        links.append({
            'link': settings.LINK_GENOME_BROWSER_GENOPEDIA + '/variation/list',
            'tags': str(variation_records),
            'title': 'Variation',
            'description': 'Total of variations'
        })
        links.append({
            'link': settings.LINK_GENOME_BROWSER_GENOPEDIA + '/gene/list',
            'tags': str(gene_records),
            'title': 'Gene',
            'description': 'Total of genes'
        })
        links.append({
            'link': settings.LINK_GENOME_BROWSER_GENOPEDIA + '/disease/list',
            'tags': str(disease_records),
            'title': 'Disease',
            'description': 'Total of diseases'
        })
        links.append({
            'link': settings.LINK_GENOME_BROWSER_GENOPEDIA + '/trait/list',
            'tags': str(trait_records),
            'title': 'Trait',
            'description': 'Total of traits'
        })
        links.append({
            'link': settings.LINK_GENOME_BROWSER_GENOPEDIA + '/treatment/list',
            'tags': str(treatment_records),
            'title': 'Treatment',
            'description': 'Total of treatments'
        })
        data.append({
            'links': links
        })
        return (data)

class UnstableBlocks(handlers.standard.GetHandler):
    def get_data(self, data):
        records = []
        block_version = VariationBlockVersion.objects.filter(is_stable=False, is_disabled=False)
        if block_version:
            for item in block_version:
                block = VariationBlock.objects.get(pk=item.variation_block_id)
                records.append({
                    'timestamp':    item.created_at,
                    'title':        block.title,
                    'page':         'Variation',
                    'kind':         block.kind
                })
        block_version = VariationBlockAliasVersion.objects.filter(is_stable=False, is_disabled=False)
        if block_version:
            for item in block_version:
                block = VariationBlock.objects.get(pk=item.variation_block_id)
                records.append({
                    'timestamp':    item.created_at,
                    'title':        block.title,
                    'page':         'Variation',
                    'kind':         block.kind
                })
        block_version = VariationBlockEffectVersion.objects.filter(is_stable=False, is_disabled=False)
        if block_version:
            for item in block_version:
                block = VariationBlock.objects.get(pk=item.variation_block_id)
                records.append({
                    'timestamp':    item.created_at,
                    'title':        block.title,
                    'page':         'Variation',
                    'kind':         block.kind
                })
        block_version = VariationBlockFrequencyVersion.objects.filter(is_stable=False, is_disabled=False)
        if block_version:
            for item in block_version:
                block = VariationBlock.objects.get(pk=item.variation_block_id)
                records.append({
                    'timestamp':    item.created_at,
                    'title':        block.title,
                    'page':         'Variation',
                    'kind':         block.kind
                })
        block_version = VariationBlockInfoboxVersion.objects.filter(is_stable=False, is_disabled=False)
        if block_version:
            for item in block_version:
                block = VariationBlock.objects.get(pk=item.variation_block_id)
                records.append({
                    'timestamp':    item.created_at,
                    'title':        block.title,
                    'page':         'Variation',
                    'kind':         block.kind
                })
        block_version = VariationBlockPublicationVersion.objects.filter(is_stable=False, is_disabled=False)
        if block_version:
            for item in block_version:
                block = VariationBlock.objects.get(pk=item.variation_block_id)
                records.append({
                    'timestamp':    item.created_at,
                    'title':        block.title,
                    'page':         'Variation',
                    'kind':         block.kind
                })
        block_version = TreatmentBlockVersion.objects.filter(is_stable=False, is_disabled=False)
        if block_version:
            for item in block_version:
                block = TreatmentBlock.objects.get(pk=item.treatment_block_id)
                records.append({
                    'timestamp':    item.created_at,
                    'title':        block.title,
                    'page':         'Treatment',
                    'kind':         block.kind
                })
        block_version = TreatmentBlockAliasVersion.objects.filter(is_stable=False, is_disabled=False)
        if block_version:
            for item in block_version:
                block = TreatmentBlock.objects.get(pk=item.treatment_block_id)
                records.append({
                    'timestamp':    item.created_at,
                    'title':        block.title,
                    'page':         'Treatment',
                    'kind':         block.kind
                })
        block_version = TreatmentBlockPublicationVersion.objects.filter(is_stable=False, is_disabled=False)
        if block_version:
            for item in block_version:
                block = TreatmentBlock.objects.get(pk=item.treatment_block_id)
                records.append({
                    'timestamp':    item.created_at,
                    'title':        block.title,
                    'page':         'Treatment',
                    'kind':         block.kind
                })
        block_version = TraitBlockVersion.objects.filter(is_stable=False, is_disabled=False)
        if block_version:
            for item in block_version:
                block = TraitBlock.objects.get(pk=item.trait_block_id)
                records.append({
                    'timestamp':    item.created_at,
                    'title':        block.title,
                    'page':         'Trait',
                    'kind':         block.kind
                })
        block_version = TraitBlockAliasVersion.objects.filter(is_stable=False, is_disabled=False)
        if block_version:
            for item in block_version:
                block = TraitBlock.objects.get(pk=item.trait_block_id)
                records.append({
                    'timestamp':    item.created_at,
                    'title':        block.title,
                    'page':         'Trait',
                    'kind':         block.kind
                })
        block_version = TraitBlockPublicationVersion.objects.filter(is_stable=False, is_disabled=False)
        if block_version:
            for item in block_version:
                block = TraitBlock.objects.get(pk=item.trait_block_id)
                records.append({
                    'timestamp':    item.created_at,
                    'title':        block.title,
                    'page':         'Trait',
                    'kind':         block.kind
                })
        block_version = DiseaseBlockVersion.objects.filter(is_stable=False, is_disabled=False)
        if block_version:
            for item in block_version:
                block = DiseaseBlock.objects.get(pk=item.disease_block_id)
                records.append({
                    'timestamp':    item.created_at,
                    'title':        block.title,
                    'page':         'Disease',
                    'kind':         block.kind
                })
        block_version = DiseaseBlockAliasVersion.objects.filter(is_stable=False, is_disabled=False)
        if block_version:
            for item in block_version:
                block = DiseaseBlock.objects.get(pk=item.disease_block_id)
                records.append({
                    'timestamp':    item.created_at,
                    'title':        block.title,
                    'page':         'Disease',
                    'kind':         block.kind
                })
        block_version = DiseaseBlockPublicationVersion.objects.filter(is_stable=False, is_disabled=False)
        if block_version:
            for item in block_version:
                block = DiseaseBlock.objects.get(pk=item.disease_block_id)
                records.append({
                    'timestamp':    item.created_at,
                    'title':        block.title,
                    'page':         'Disease',
                    'kind':         block.kind
                })
        block_version = GeneBlockVersion.objects.filter(is_stable=False, is_disabled=False)
        if block_version:
            for item in block_version:
                block = GeneBlock.objects.get(pk=item.gene_block_id)
                records.append({
                    'timestamp':    item.created_at,
                    'title':        block.title,
                    'page':         'Gene',
                    'kind':         block.kind
                })
        block_version = GeneBlockAliasVersion.objects.filter(is_stable=False, is_disabled=False)
        if block_version:
            for item in block_version:
                block = GeneBlock.objects.get(pk=item.gene_block_id)
                records.append({
                    'timestamp':    item.created_at,
                    'title':        block.title,
                    'page':         'Gene',
                    'kind':         block.kind
                })
        block_version = GeneBlockPublicationVersion.objects.filter(is_stable=False, is_disabled=False)
        if block_version:
            for item in block_version:
                block = GeneBlock.objects.get(pk=item.gene_block_id)
                records.append({
                    'timestamp':    item.created_at,
                    'title':        block.title,
                    'page':         'Gene',
                    'kind':         block.kind
                })
        block_version = GeneBlockEffectVersion.objects.filter(is_stable=False, is_disabled=False)
        if block_version:
            for item in block_version:
                block = GeneBlock.objects.get(pk=item.gene_block_id)
                records.append({
                    'timestamp':    item.created_at,
                    'title':        block.title,
                    'page':         'Gene',
                    'kind':         block.kind
                })
        block_version = GeneBlockInfoboxVersion.objects.filter(is_stable=False, is_disabled=False)
        if block_version:
            for item in block_version:
                block = GeneBlock.objects.get(pk=item.gene_block_id)
                records.append({
                    'timestamp':    item.created_at,
                    'title':        block.title,
                    'page':         'Gene',
                    'kind':         block.kind
                })
        return {
            'records': records
        }

class ListBlocks(handlers.standard.GetHandler):
    def get_data(self, data):
        records = []
        stable = []
        entity_id = ''
        # Random unstable version
        block_version = VariationBlockVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
        if block_version:
            for item in block_version:
                entity_id = item.variation_id
                block = VariationBlock.objects.get(pk=item.variation_block_id)
                variation = Variation.objects.get(pk=item.variation_id)
                records.append({
                    'id':           item.id,
                    'timestamp':    item.created_at,
                    'title':        item.title,
                    'page':         'Variation',
                    'kind':         'General - Text',
                    'text':         item.text,
                    'entity':       variation.title
                })
            # Previous stable version
            block_version = VariationBlockVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, variation_id=entity_id).order_by('-created_at')[:1]
            if block_version:
                for item in block_version:
                    block = VariationBlock.objects.get(pk=item.variation_block_id)
                    variation = Variation.objects.get(pk=item.variation_id)
                    stable.append({
                        'timestamp':    item.created_at,
                        'title':        item.title,
                        'page':         'Variation',
                        'kind':         'General - Text',
                        'text':         item.text,
                        'entity':       variation.title
                    })
        else:
            block_version = VariationBlockAliasVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
            if block_version:
                for item in block_version:
                    entity_id = item.variation_id
                    alias = []
                    block = VariationBlockAlias.objects.filter(variation_block_version_id=item.id)
                    for i in block:
                        alias.append(i.alias)
                    variation = Variation.objects.get(pk=item.variation_id)
                    records.append({
                        'id':           item.id,
                        'timestamp':    item.created_at,
                        'title':        'Alias',
                        'page':         'Variation',
                        'kind':         'General - Alias',
                        'alias':         alias,
                        'entity':       variation.title
                    })
                # Previous stable version
                block_version = VariationBlockAliasVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, variation_id=entity_id).order_by('-created_at')[:1]
                if block_version:
                    for item in block_version:
                        alias = []
                        block = VariationBlockAlias.objects.filter(variation_block_version_id=item.id)
                        for i in block:
                            alias.append(i.alias)
                        variation = Variation.objects.get(pk=item.variation_id)
                        stable.append({
                            'timestamp':    item.created_at,
                            'title':        'Alias',
                            'page':         'Variation',
                            'kind':         'General - Alias',
                            'alias':         alias,
                            'entity':       variation.title
                        })
            else:
                block_version = VariationBlockEffectVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
                if block_version:
                    for item in block_version:
                        entity_id = item.variation_id
                        effects = {}
                        block = VariationBlockEffect.objects.filter(variation_block_version_id=item.id)
                        if block:
                            effects['content'] = []
                            for i in block:
                                html = '<tr>'
                                html += '<td>' + i.popcode + '</td>'
                                html += '<td>' + i.genotype + '</td>'
                                html += '<td>' + i.risk + '</td>'
                                html += '<td>' + str(i.odd_ratio) + '</td>'
                                html += '<td>' + i.evidences + '</td>'
                                html += '<td>' + i.pmid + '</td>'
                                html += '</tr>'
                                effects['content'].append(html)
                            effects['header'] = ['popcode', 'genotype', 'risk', 'odd_ratio', 'evidences', 'pmid']

                        variation = Variation.objects.get(pk=item.variation_id)
                        records.append({
                            'id':           item.id,
                            'timestamp':    item.created_at,
                            'title':        'Alias',
                            'page':         'Variation',
                            'kind':         'Variation - Effects',
                            'effects':      effects,
                            'entity':       variation.title
                        })
                    # Previous stable version
                    block_version = VariationBlockEffectVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, variation_id=entity_id).order_by('-created_at')[:1]
                    if block_version:
                        for item in block_version:
                            effects = {}
                            block = VariationBlockEffect.objects.filter(variation_block_version_id=item.id)
                            if block:
                                effects['content'] = []
                                for i in block:
                                    html = '<tr>'
                                    html += '<td>' + i.popcode + '</td>'
                                    html += '<td>' + i.genotype + '</td>'
                                    html += '<td>' + i.risk + '</td>'
                                    html += '<td>' + str(i.odd_ratio) + '</td>'
                                    html += '<td>' + i.evidences + '</td>'
                                    html += '<td>' + i.pmid + '</td>'
                                    html += '</tr>'
                                    effects['content'].append(html)
                                effects['header'] = ['popcode', 'genotype', 'risk', 'odd_ratio', 'evidences', 'pmid']
                            variation = Variation.objects.get(pk=item.variation_id)
                            stable.append({
                                'timestamp':    item.created_at,
                                'title':        'Alias',
                                'page':         'Variation',
                                'kind':         'Variation - Effects',
                                'effects':      effects,
                                'entity':       variation.title
                            })
                else:
                    block_version = VariationBlockFrequencyVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
                    if block_version:
                        for item in block_version:
                            entity_id = item.variation_id
                            frequencies = []
                            block = VariationBlockFrequency.objects.filter(variation_block_version_id=item.id)
                            for i in block:
                                frequencies.append({
                                    'popcode':              i.popcode,
                                    'genotype_count_00':    i.genotype_count_00,
                                    'genotype_count_01':    i.genotype_count_01,
                                    'genotype_count_11':    i.genotype_count_11
                                })
                            variation = Variation.objects.get(pk=item.variation_id)
                            records.append({
                                'id':           item.id,
                                'timestamp':    item.created_at,
                                'title':        'Alias',
                                'page':         'Variation',
                                'kind':         'Variation - Frequency',
                                'frequencies':  frequencies,
                                'entity':       variation.title
                            })
                        # Previous stable version
                        block_version = VariationBlockFrequencyVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, variation_id=entity_id).order_by('-created_at')[:1]
                        if block_version:
                            for item in block_version:
                                frequencies = []
                                block = VariationBlockFrequency.objects.filter(variation_block_version_id=item.id)
                                for i in block:
                                    frequencies.append({
                                        'popcode':              i.popcode,
                                        'genotype_count_00':    i.genotype_count_00,
                                        'genotype_count_01':    i.genotype_count_01,
                                        'genotype_count_11':    i.genotype_count_11
                                    })
                                variation = Variation.objects.get(pk=item.variation_id)
                                stable.append({
                                    'timestamp':    item.created_at,
                                    'title':        'Alias',
                                    'page':         'Variation',
                                    'kind':         'Variation - Frequency',
                                    'frequencies':  frequencies,
                                    'entity':       variation.title
                                })
                    else:
                        block_version = VariationBlockInfoboxVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
                        if block_version:
                            for item in block_version:
                                entity_id = item.variation_id
                                infobox = []
                                block = VariationBlockInfobox.objects.filter(variation_block_version_id=item.id)
                                for i in block:
                                    infobox.append({
                                        i.key:    i.value
                                    })
                                variation = Variation.objects.get(pk=item.variation_id)
                                records.append({
                                    'id':           item.id,
                                    'timestamp':    item.created_at,
                                    'title':        'Alias',
                                    'page':         'Variation',
                                    'kind':         'Variation - Infobox',
                                    'infobox':      infobox,
                                    'entity':       variation.title
                                })
                            # Previous stable version
                            block_version = VariationBlockInfoboxVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, variation_id=entity_id).order_by('-created_at')[:1]
                            if block_version:
                                for item in block_version:
                                    infobox = []
                                    block = VariationBlockInfobox.objects.filter(variation_block_version_id=item.id)
                                    for i in block:
                                        infobox.append({
                                            i.key:    i.value
                                        })
                                    variation = Variation.objects.get(pk=item.variation_id)
                                    stable.append({
                                        'timestamp':    item.created_at,
                                        'title':        'Alias',
                                        'page':         'Variation',
                                        'kind':         'Variation - Infobox',
                                        'infobox':      infobox,
                                        'entity':       variation.title
                                    })
                        else:
                            block_version = VariationBlockPublicationVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
                            if block_version:
                                for item in block_version:
                                    entity_id = item.variation_id
                                    pub = {}
                                    pub['content'] = []
                                    block = VariationBlockPublication.objects.filter(variation_block_version_id=item.id)
                                    if block:
                                        for i in block:
                                            html = '<tr>'
                                            html += '<td>' + i.pmid + '</td>'
                                            html += '<td>' + i.doi + '</td>'
                                            html += '<td>' + i.pmc + '</td>'
                                            html += '<td>' + i.title + '</td>'
                                            html += '<td>' + i.authors + '</td>'
                                            html += '<td>' + i.journal + '</td>'
                                            html += '</tr>'
                                            pub['content'].append(html)
                                        pub['header'] = ['pmid', 'doi', 'pmc', 'title', 'authors', 'journal']
                                    variation = Variation.objects.get(pk=item.variation_id)
                                    records.append({
                                        'id':           item.id,
                                        'timestamp':    item.created_at,
                                        'title':        'Alias',
                                        'page':         'Variation',
                                        'kind':         'General - Publication',
                                        'publication':  pub,
                                        'entity':       variation.title
                                    })
                                # Previous stable version
                                block_version = VariationBlockPublicationVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, variation_id=entity_id).order_by('-created_at')[:1]
                                if block_version:
                                    for item in block_version:
                                        pub = {}
                                        pub['content'] = []
                                        block = VariationBlockPublication.objects.filter(variation_block_version_id=item.id)
                                        if block:
                                            for i in block:
                                                html = '<tr>'
                                                html += '<td>' + i.pmid + '</td>'
                                                html += '<td>' + i.doi + '</td>'
                                                html += '<td>' + i.pmc + '</td>'
                                                html += '<td>' + i.title + '</td>'
                                                html += '<td>' + i.authors + '</td>'
                                                html += '<td>' + i.journal + '</td>'
                                                html += '</tr>'
                                                pub['content'].append(html)
                                            pub['header'] = ['pmid', 'doi', 'pmc', 'title', 'authors', 'journal']
                                        variation = Variation.objects.get(pk=item.variation_id)
                                        stable.append({
                                            'timestamp':    item.created_at,
                                            'title':        'Alias',
                                            'page':         'Variation',
                                            'kind':         'General - Publication',
                                            'publication':  pub,
                                            'entity':       variation.title
                                        })
        # Treatment
        if not records:
            block_version = TreatmentBlockVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
            if block_version:
                for item in block_version:
                    entity_id = item.treatment_id
                    block = TreatmentBlock.objects.get(pk=item.treatment_block_id)
                    treatment = Treatment.objects.get(pk=item.treatment_id)
                    records.append({
                        'id':           item.id,
                        'timestamp':    item.created_at,
                        'title':        item.title,
                        'page':         'Treatment',
                        'kind':         'General - Text',
                        'text':         item.text,
                        'entity':       treatment.title
                    })
                # Previous stable version
                block_version = TreatmentBlockVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, treatment_id=entity_id).order_by('-created_at')[:1]
                if block_version:
                    for item in block_version:
                        block = TreatmentBlock.objects.get(pk=item.treatment_block_id)
                        treatment = Treatment.objects.get(pk=item.treatment_id)
                        stable.append({
                            'timestamp':    item.created_at,
                            'title':        item.title,
                            'page':         'Treatment',
                            'kind':         'General - Text',
                            'text':         item.text,
                            'entity':       treatment.title
                        })
            else:
                block_version = TreatmentBlockAliasVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
                if block_version:
                    for item in block_version:
                        entity_id = item.treatment_id
                        alias = []
                        block = TreatmentBlockAlias.objects.filter(treatment_block_version_id=item.id)
                        for i in block:
                            alias.append(i.alias)
                        treatment = Treatment.objects.get(pk=item.treatment_id)
                        records.append({
                            'id':           item.id,
                            'timestamp':    item.created_at,
                            'title':        'Alias',
                            'page':         'Treatment',
                            'kind':         'General - Alias',
                            'alias':         alias,
                            'entity':        treatment.title
                        })
                    # Previous stable version
                    block_version = TreatmentBlockAliasVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, treatment_id=entity_id).order_by('-created_at')[:1]
                    if block_version:
                        for item in block_version:
                            alias = []
                            block = TreatmentBlockAlias.objects.filter(treatment_block_version_id=item.id)
                            for i in block:
                                alias.append(i.alias)
                            treatment = Treatment.objects.get(pk=item.treatment_id)
                            stable.append({
                                'timestamp':    item.created_at,
                                'title':        'Alias',
                                'page':         'Treatment',
                                'kind':         'General - Alias',
                                'alias':         alias,
                                'entity':        treatment.title
                            })
                else:
                    block_version = TreatmentBlockPublicationVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
                    if block_version:
                        for item in block_version:
                            entity_id = item.treatment_id
                            pub = {}
                            pub['content'] = []
                            block = TreatmentBlockPublication.objects.filter(treatment_block_version_id=item.id)
                            if block:
                                for i in block:
                                    html = '<tr>'
                                    html += '<td>' + i.pmid + '</td>'
                                    html += '<td>' + i.doi + '</td>'
                                    html += '<td>' + i.pmc + '</td>'
                                    html += '<td>' + i.title + '</td>'
                                    html += '<td>' + i.authors + '</td>'
                                    html += '<td>' + i.journal + '</td>'
                                    html += '</tr>'
                                    pub['content'].append(html)
                                pub['header'] = ['pmid', 'doi', 'pmc', 'title', 'authors', 'journal']
                            treatment = Treatment.objects.get(pk=item.treatment_id)
                            records.append({
                                'id':           item.id,
                                'timestamp':    item.created_at,
                                'title':        'Alias',
                                'page':         'Treatment',
                                'kind':         'General - Publication',
                                'publication':  pub,
                                'entity':       treatment.title
                            })
                        # Previous stable version
                        block_version = TreatmentBlockPublicationVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, treatment_id=entity_id).order_by('-created_at')[:1]
                        if block_version:
                            for item in block_version:
                                pub = {}
                                pub['content'] = []
                                block = TreatmentBlockPublication.objects.filter(treatment_block_version_id=item.id)
                                if block:
                                    for i in block:
                                        html = '<tr>'
                                        html += '<td>' + i.pmid + '</td>'
                                        html += '<td>' + i.doi + '</td>'
                                        html += '<td>' + i.pmc + '</td>'
                                        html += '<td>' + i.title + '</td>'
                                        html += '<td>' + i.authors + '</td>'
                                        html += '<td>' + i.journal + '</td>'
                                        html += '</tr>'
                                        pub['content'].append(html)
                                    pub['header'] = ['pmid', 'doi', 'pmc', 'title', 'authors', 'journal']
                                treatment = Treatment.objects.get(pk=item.treatment_id)
                                stable.append({
                                    'timestamp':    item.created_at,
                                    'title':        'Alias',
                                    'page':         'Treatment',
                                    'kind':         'General - Publication',
                                    'publication':  pub,
                                    'entity':       treatment.title
                                })
        # Trait
        if not records:
            block_version = TraitBlockVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
            if block_version:
                for item in block_version:
                    entity_id = item.trait_id
                    block = TraitBlock.objects.get(pk=item.trait_block_id)
                    trait = Trait.objects.get(pk=item.trait_id)
                    records.append({
                        'id':           item.id,
                        'timestamp':    item.created_at,
                        'title':        item.title,
                        'page':         'Trait',
                        'kind':         'General - Text',
                        'text':         item.text,
                        'entity':       trait.title
                    })
                # Previous stable version
                block_version = TraitBlockVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, trait_id=entity_id).order_by('-created_at')[:1]
                if block_version:
                    for item in block_version:
                        block = TraitBlock.objects.get(pk=item.trait_block_id)
                        trait = Trait.objects.get(pk=item.trait_id)
                        stable.append({
                            'timestamp':    item.created_at,
                            'title':        item.title,
                            'page':         'Trait',
                            'kind':         'General - Text',
                            'text':         item.text,
                            'entity':       trait.title
                        })
            else:
                block_version = TraitBlockAliasVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
                if block_version:
                    for item in block_version:
                        entity_id = item.trait_id
                        alias = []
                        block = TraitBlockAlias.objects.filter(trait_block_version_id=item.id)
                        for i in block:
                            alias.append(i.alias)
                        trait = Trait.objects.get(pk=item.trait_id)
                        records.append({
                            'id':           item.id,
                            'timestamp':    item.created_at,
                            'title':        'Alias',
                            'page':         'Trait',
                            'kind':         'General - Alias',
                            'alias':         alias,
                            'entity':        trait.title
                        })
                    # Previous stable version
                    block_version = TraitBlockAliasVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, trait_id=entity_id).order_by('-created_at')[:1]
                    if block_version:
                        for item in block_version:
                            alias = []
                            block = TraitBlockAlias.objects.filter(trait_block_version_id=item.id)
                            for i in block:
                                alias.append(i.alias)
                            trait = Trait.objects.get(pk=item.trait_id)
                            stable.append({
                                'timestamp':    item.created_at,
                                'title':        'Alias',
                                'page':         'Trait',
                                'kind':         'General - Alias',
                                'alias':         alias,
                                'entity':        trait.title
                            })
                else:
                    block_version = TraitBlockPublicationVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
                    if block_version:
                        for item in block_version:
                            entity_id = item.trait_id
                            pub = {}
                            pub['content'] = []
                            block = TraitBlockPublication.objects.filter(trait_block_version_id=item.id)
                            if block:
                                for i in block:
                                    html = '<tr>'
                                    html += '<td>' + i.pmid + '</td>'
                                    html += '<td>' + i.doi + '</td>'
                                    html += '<td>' + i.pmc + '</td>'
                                    html += '<td>' + i.title + '</td>'
                                    html += '<td>' + i.authors + '</td>'
                                    html += '<td>' + i.journal + '</td>'
                                    html += '</tr>'
                                    pub['content'].append(html)
                                pub['header'] = ['pmid', 'doi', 'pmc', 'title', 'authors', 'journal']
                            trait = Trait.objects.get(pk=item.trait_id)
                            records.append({
                                'id':           item.id,
                                'timestamp':    item.created_at,
                                'title':        'Alias',
                                'page':         'Trait',
                                'kind':         'General - Alias',
                                'publication':  pub,
                                'entity':       trait.title
                            })
                        # Previous stable version
                        block_version = TraitBlockPublicationVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, trait_id=entity_id).order_by('-created_at')[:1]
                        if block_version:
                            for item in block_version:
                                pub = {}
                                pub['content'] = []
                                block = TraitBlockPublication.objects.filter(trait_block_version_id=item.id)
                                if block:
                                    for i in block:
                                        html = '<tr>'
                                        html += '<td>' + i.pmid + '</td>'
                                        html += '<td>' + i.doi + '</td>'
                                        html += '<td>' + i.pmc + '</td>'
                                        html += '<td>' + i.title + '</td>'
                                        html += '<td>' + i.authors + '</td>'
                                        html += '<td>' + i.journal + '</td>'
                                        html += '</tr>'
                                        pub['content'].append(html)
                                    pub['header'] = ['pmid', 'doi', 'pmc', 'title', 'authors', 'journal']
                                trait = Trait.objects.get(pk=item.trait_id)
                                stable.append({
                                    'timestamp':    item.created_at,
                                    'title':        'Alias',
                                    'page':         'Trait',
                                    'kind':         'General - Alias',
                                    'publication':  pub,
                                    'entity':       trait.title
                                })
        # Disease
        if not records:
            block_version = DiseaseBlockVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
            if block_version:
                for item in block_version:
                    entity_id = item.disease_id
                    block = DiseaseBlock.objects.get(pk=item.disease_block_id)
                    disease = Disease.objects.get(pk=item.disease_id)
                    records.append({
                        'id':           item.id,
                        'timestamp':    item.created_at,
                        'title':        item.title,
                        'page':         'Disease',
                        'kind':         'General - Text',
                        'text':         item.text,
                        'entity':       disease.title
                    })
                # Previous stable version
                block_version = DiseaseBlockVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, disease_id=entity_id).order_by('-created_at')[:1]
                if block_version:
                    for item in block_version:
                        block = DiseaseBlock.objects.get(pk=item.disease_block_id)
                        disease = Disease.objects.get(pk=item.disease_id)
                        stable.append({
                            'timestamp':    item.created_at,
                            'title':        item.title,
                            'page':         'Disease',
                            'kind':         'General - Text',
                            'text':         item.text,
                            'entity':       disease.title
                        })
            else:
                block_version = DiseaseBlockAliasVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
                if block_version:
                    for item in block_version:
                        entity_id = item.disease_id
                        alias = []
                        block = DiseaseBlockAlias.objects.filter(disease_block_version_id=item.id)
                        for i in block:
                            alias.append(i.alias)
                        disease = Disease.objects.get(pk=item.disease_id)
                        records.append({
                            'id':           item.id,
                            'timestamp':    item.created_at,
                            'title':        'Alias',
                            'page':         'Disease',
                            'kind':         'General - Alias',
                            'alias':         alias,
                            'entity':        disease.title
                        })
                    # Previous stable version
                    block_version = DiseaseBlockAliasVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, disease_id=entity_id).order_by('-created_at')[:1]
                    if block_version:
                        for item in block_version:
                            alias = []
                            block = DiseaseBlockAlias.objects.filter(disease_block_version_id=item.id)
                            for i in block:
                                alias.append(i.alias)
                            disease = Disease.objects.get(pk=item.disease_id)
                            stable.append({
                                'timestamp':    item.created_at,
                                'title':        'Alias',
                                'page':         'Disease',
                                'kind':         'General - Alias',
                                'alias':         alias,
                                'entity':        disease.title
                            })
                else:
                    block_version = DiseaseBlockPublicationVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
                    if block_version:
                        for item in block_version:
                            entity_id = item.disease_id
                            pub = {}
                            pub['content'] = []
                            block = DiseaseBlockPublication.objects.filter(disease_block_version_id=item.id)
                            if block:
                                for i in block:
                                    html = '<tr>'
                                    html += '<td>' + i.pmid + '</td>'
                                    html += '<td>' + i.doi + '</td>'
                                    html += '<td>' + i.pmc + '</td>'
                                    html += '<td>' + i.title + '</td>'
                                    html += '<td>' + i.authors + '</td>'
                                    html += '<td>' + i.journal + '</td>'
                                    html += '</tr>'
                                    pub['content'].append(html)
                                pub['header'] = ['pmid', 'doi', 'pmc', 'title', 'authors', 'journal']
                            disease = Disease.objects.get(pk=item.disease_id)
                            records.append({
                                'id':           item.id,
                                'timestamp':    item.created_at,
                                'title':        'Alias',
                                'page':         'Disease',
                                'kind':         'General - Publication',
                                'publication':  pub,
                                'entity':       disease.title
                            })
                        # Previous stable version
                        block_version = DiseaseBlockPublicationVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, disease_id=entity_id).order_by('-created_at')[:1]
                        if block_version:
                            for item in block_version:
                                pub = {}
                                pub['content'] = []
                                block = DiseaseBlockPublication.objects.filter(disease_block_version_id=item.id)
                                if block:
                                    for i in block:
                                        html = '<tr>'
                                        html += '<td>' + i.pmid + '</td>'
                                        html += '<td>' + i.doi + '</td>'
                                        html += '<td>' + i.pmc + '</td>'
                                        html += '<td>' + i.title + '</td>'
                                        html += '<td>' + i.authors + '</td>'
                                        html += '<td>' + i.journal + '</td>'
                                        html += '</tr>'
                                        pub['content'].append(html)
                                    pub['header'] = ['pmid', 'doi', 'pmc', 'title', 'authors', 'journal']
                                disease = Disease.objects.get(pk=item.disease_id)
                                stable.append({
                                    'timestamp':    item.created_at,
                                    'title':        'Alias',
                                    'page':         'Disease',
                                    'kind':         'General - Publication',
                                    'publication':  pub,
                                    'entity':       disease.title
                                })
        # Gene
        if not records:
            block_version = GeneBlockVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
            if block_version:
                for item in block_version:
                    entity_id = item.gene_id
                    block = GeneBlock.objects.get(pk=item.gene_block_id)
                    gene = Gene.objects.get(pk=item.gene_id)
                    records.append({
                        'id':           item.id,
                        'timestamp':    item.created_at,
                        'title':        item.title,
                        'page':         'Gene',
                        'kind':         'General - Text',
                        'text':         item.text,
                        'entity':       gene.title
                    })
                # Previous stable version
                block_version = GeneBlockVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, gene_id=entity_id).order_by('-created_at')[:1]
                if block_version:
                    for item in block_version:
                        block = GeneBlock.objects.get(pk=item.gene_block_id)
                        gene = Gene.objects.get(pk=item.gene_id)
                        stable.append({
                            'timestamp':    item.created_at,
                            'title':        item.title,
                            'page':         'Gene',
                            'kind':         'General - Text',
                            'text':         item.text,
                            'entity':       gene.title
                        })
            else:
                block_version = GeneBlockAliasVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
                if block_version:
                    for item in block_version:
                        entity_id = item.gene_id
                        alias = []
                        block = GeneBlockAlias.objects.filter(gene_block_version_id=item.id)
                        for i in block:
                            alias.append(i.alias)
                        gene = Gene.objects.get(pk=item.gene_id)
                        records.append({
                            'id':           item.id,
                            'timestamp':    item.created_at,
                            'title':        'Alias',
                            'page':         'Gene',
                            'kind':         'General - Alias',
                            'alias':         alias,
                            'entity':       gene.title
                        })
                    # Previous stable version
                    block_version = GeneBlockAliasVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, gene_id=entity_id).order_by('-created_at')[:1]
                    if block_version:
                        for item in block_version:
                            alias = []
                            block = GeneBlockAlias.objects.filter(gene_block_version_id=item.id)
                            for i in block:
                                alias.append(i.alias)
                            gene = Gene.objects.get(pk=item.gene_id)
                            stable.append({
                                'timestamp':    item.created_at,
                                'title':        'Alias',
                                'page':         'Gene',
                                'kind':         'General - Alias',
                                'alias':         alias,
                                'entity':       gene.title
                            })
                else:
                    block_version = GeneBlockEffectVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
                    if block_version:
                        for item in block_version:
                            entity_id = item.gene_id
                            effects = {}
                            block = GeneBlockEffect.objects.filter(gene_block_version_id=item.id)
                            if block:
                                effects['content'] = []
                                for i in block:
                                    html = '<tr>'
                                    html += '<td>' + i.type + '</td>'
                                    html += '<td>' + i.effect + '</td>'
                                    html += '<td>' + i.evidences + '</td>'
                                    html += '<td>' + i.publication + '</td>'
                                    html += '</tr>'
                                    effects['content'].append(html)
                                effects['header'] = ['type', 'effect', 'evidences', 'publication']
                            gene = Gene.objects.get(pk=item.gene_id)
                            records.append({
                                'id':           item.id,
                                'timestamp':    item.created_at,
                                'title':        'Alias',
                                'page':         'Gene',
                                'kind':         'Gene - Effect',
                                'effects':      effects,
                                'entity':       gene.title
                            })
                        # Previous stable version
                        block_version = GeneBlockEffectVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, gene_id=entity_id).order_by('-created_at')[:1]
                        if block_version:
                            for item in block_version:
                                effects = {}
                                block = GeneBlockEffect.objects.filter(gene_block_version_id=item.id)
                                if block:
                                    effects['content'] = []
                                    for i in block:
                                        html = '<tr>'
                                        html += '<td>' + i.type + '</td>'
                                        html += '<td>' + i.effect + '</td>'
                                        html += '<td>' + i.evidences + '</td>'
                                        html += '<td>' + i.publication + '</td>'
                                        html += '</tr>'
                                        effects['content'].append(html)
                                    effects['header'] = ['type', 'effect', 'evidences', 'publication']
                                gene = Gene.objects.get(pk=item.gene_id)
                                stable.append({
                                    'timestamp':    item.created_at,
                                    'title':        'Alias',
                                    'page':         'Gene',
                                    'kind':         'Gene - Effect',
                                    'effects':      effects,
                                    'entity':       gene.title
                                })
                    else:
                        block_version = GeneBlockInfoboxVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
                        if block_version:
                            for item in block_version:
                                entity_id = item.gene_id
                                infobox = []
                                block = GeneBlockInfobox.objects.filter(gene_block_version_id=item.id)
                                for i in block:
                                    infobox.append({
                                        'description':      i.description,
                                        'chromosome':       i.chromosome,
                                        'start':            i.start,
                                        'end':              i.end,
                                        'number_of_exons':  i.number_of_exons,
                                        'protein_products': i.protein_products
                                    })
                                gene = Gene.objects.get(pk=item.gene_id)
                                records.append({
                                    'id':           item.id,
                                    'timestamp':    item.created_at,
                                    'title':        'Alias',
                                    'page':         'Gene',
                                    'kind':         'Gene - Infobox',
                                    'infobox':      infobox,
                                    'entity':       gene.title
                                })
                            # Previous stable version
                            block_version = GeneBlockInfoboxVersion.objects.filter(is_stable=True,version_status='active', is_disabled=False, gene_id=entity_id).order_by('-created_at')[:1]
                            if block_version:
                                for item in block_version:
                                    infobox = []
                                    block = GeneBlockInfobox.objects.filter(gene_block_version_id=item.id)
                                    for i in block:
                                        infobox.append({
                                            'description':      i.description,
                                            'chromosome':       i.chromosome,
                                            'start':            i.start,
                                            'end':              i.end,
                                            'number_of_exons':  i.number_of_exons,
                                            'protein_products': i.protein_products
                                        })
                                    gene = Gene.objects.get(pk=item.gene_id)
                                    stable.append({
                                        'timestamp':    item.created_at,
                                        'title':        'Alias',
                                        'page':         'Gene',
                                        'kind':         'Gene - Infobox',
                                        'infobox':      infobox,
                                        'entity':       gene.title
                                    })
                        else:
                            block_version = GeneBlockPublicationVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
                            if block_version:
                                for item in block_version:
                                    entity_id = item.gene_id
                                    pub = {}
                                    pub['content'] = []
                                    block = GeneBlockPublication.objects.filter(gene_block_version_id=item.id)
                                    if block:
                                        for i in block:
                                            html = '<tr>'
                                            html += '<td>' + i.pmid + '</td>'
                                            html += '<td>' + i.doi + '</td>'
                                            html += '<td>' + i.pmc + '</td>'
                                            html += '<td>' + i.title + '</td>'
                                            html += '<td>' + i.authors + '</td>'
                                            html += '<td>' + i.journal + '</td>'
                                            html += '</tr>'
                                            pub['content'].append(html)
                                        pub['header'] = ['pmid', 'doi', 'pmc', 'title', 'authors', 'journal']
                                    gene = Gene.objects.get(pk=item.gene_id)
                                    records.append({
                                        'id':           item.id,
                                        'timestamp':    item.created_at,
                                        'title':        'Alias',
                                        'page':         'Gene',
                                        'kind':         'General - Publication',
                                        'publication':  pub,
                                        'entity':       gene.title
                                    })
                                # Previous stable version
                                block_version = GeneBlockPublicationVersion.objects.filter(is_stable=True, version_status='Active', is_disabled=False, gene_id=entity_id).order_by('-created_at')[:1]
                                if block_version:
                                    for item in block_version:
                                        pub = {}
                                        pub['content'] = []
                                        block = GeneBlockPublication.objects.filter(gene_block_version_id=item.id)
                                        if block:
                                            for i in block:
                                                html = '<tr>'
                                                html += '<td>' + i.pmid + '</td>'
                                                html += '<td>' + i.doi + '</td>'
                                                html += '<td>' + i.pmc + '</td>'
                                                html += '<td>' + i.title + '</td>'
                                                html += '<td>' + i.authors + '</td>'
                                                html += '<td>' + i.journal + '</td>'
                                                html += '</tr>'
                                                pub['content'].append(html)
                                            pub['header'] = ['pmid', 'doi', 'pmc', 'title', 'authors', 'journal']
                                        gene = Gene.objects.get(pk=item.gene_id)
                                        stable.append({
                                            'timestamp':    item.created_at,
                                            'title':        'Alias',
                                            'page':         'Gene',
                                            'kind':         'General - Publication',
                                            'publication':  pub,
                                            'entity':       gene.title
                                        })

        return {
            'records': records,
            'stable': stable
        }

class GetBlockValidationGene(handlers.standard.GetHandler):
    def get_data(self, data):
        records = []
        stable = []
        entity_id = ''

        block_gene = GeneBlock.objects.get(pk=data['id'])
        # Gene
        if block_gene.kind == 'general_text':
            block_version = GeneBlockVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
            if block_version:
                for item in block_version:
                    entity_id = item.gene_id
                    block = GeneBlock.objects.get(pk=item.gene_block_id)
                    gene = Gene.objects.get(pk=item.gene_id)
                    records.append({
                        'id':           item.id,
                        'timestamp':    item.created_at,
                        'title':        item.title,
                        'page':         'Gene',
                        'kind':         'General - Text',
                        'text':         item.text,
                        'entity':       gene.title
                    })
                # Previous stable version
                block_version = GeneBlockVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, gene_id=entity_id).order_by('-created_at')[:1]
                if block_version:
                    for item in block_version:
                        block = GeneBlock.objects.get(pk=item.gene_block_id)
                        gene = Gene.objects.get(pk=item.gene_id)
                        stable.append({
                            'timestamp':    item.created_at,
                            'title':        item.title,
                            'page':         'Gene',
                            'kind':         'General - Text',
                            'text':         item.text,
                            'entity':       gene.title
                        })
        if block_gene.kind == 'general_alias':
            block_version = GeneBlockAliasVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
            if block_version:
                for item in block_version:
                    entity_id = item.gene_id
                    alias = []
                    block = GeneBlockAlias.objects.filter(gene_block_version_id=item.id)
                    for i in block:
                        alias.append(i.alias)
                    gene = Gene.objects.get(pk=item.gene_id)
                    records.append({
                        'id':           item.id,
                        'timestamp':    item.created_at,
                        'title':        'Alias',
                        'page':         'Gene',
                        'kind':         'General - Alias',
                        'alias':         alias,
                        'entity':       gene.title
                    })
                # Previous stable version
                block_version = GeneBlockAliasVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, gene_id=entity_id).order_by('-created_at')[:1]
                if block_version:
                    for item in block_version:
                        alias = []
                        block = GeneBlockAlias.objects.filter(gene_block_version_id=item.id)
                        for i in block:
                            alias.append(i.alias)
                        gene = Gene.objects.get(pk=item.gene_id)
                        stable.append({
                            'timestamp':    item.created_at,
                            'title':        'Alias',
                            'page':         'Gene',
                            'kind':         'General - Alias',
                            'alias':         alias,
                            'entity':       gene.title
                        })
        if block_gene.kind == 'gene_effect':
            block_version = GeneBlockEffectVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
            if block_version:
                for item in block_version:
                    entity_id = item.gene_id
                    effects = {}
                    block = GeneBlockEffect.objects.filter(gene_block_version_id=item.id)
                    if block:
                        effects['content'] = []
                        for i in block:
                            html = '<tr>'
                            html += '<td>' + i.type + '</td>'
                            html += '<td>' + i.effect + '</td>'
                            html += '<td>' + i.evidences + '</td>'
                            html += '<td>' + i.publication + '</td>'
                            html += '</tr>'
                            effects['content'].append(html)
                        effects['header'] = ['type', 'effect', 'evidences', 'publication']
                    gene = Gene.objects.get(pk=item.gene_id)
                    records.append({
                        'id':           item.id,
                        'timestamp':    item.created_at,
                        'title':        'Alias',
                        'page':         'Gene',
                        'kind':         'Gene - Effect',
                        'effects':      effects,
                        'entity':       gene.title
                    })
                # Previous stable version
                block_version = GeneBlockEffectVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, gene_id=entity_id).order_by('-created_at')[:1]
                if block_version:
                    for item in block_version:
                        effects = {}
                        block = GeneBlockEffect.objects.filter(gene_block_version_id=item.id)
                        if block:
                            effects['content'] = []
                            for i in block:
                                html = '<tr>'
                                html += '<td>' + i.type + '</td>'
                                html += '<td>' + i.effect + '</td>'
                                html += '<td>' + i.evidences + '</td>'
                                html += '<td>' + i.publication + '</td>'
                                html += '</tr>'
                                effects['content'].append(html)
                            effects['header'] = ['type', 'effect', 'evidences', 'publication']
                        gene = Gene.objects.get(pk=item.gene_id)
                        stable.append({
                            'timestamp':    item.created_at,
                            'title':        'Alias',
                            'page':         'Gene',
                            'kind':         'Gene - Effect',
                            'effects':      effects,
                            'entity':       gene.title
                        })
        if block_gene.kind == 'gene_infobox':
            block_version = GeneBlockInfoboxVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
            if block_version:
                for item in block_version:
                    entity_id = item.gene_id
                    infobox = []
                    block = GeneBlockInfobox.objects.filter(gene_block_version_id=item.id)
                    for i in block:
                        infobox.append({
                            'description':      i.description,
                            'chromosome':       i.chromosome,
                            'start':            i.start,
                            'end':              i.end,
                            'number_of_exons':  i.number_of_exons,
                            'protein_products': i.protein_products
                        })
                    gene = Gene.objects.get(pk=item.gene_id)
                    records.append({
                        'id':           item.id,
                        'timestamp':    item.created_at,
                        'title':        'Alias',
                        'page':         'Gene',
                        'kind':         'Gene - Infobox',
                        'infobox':      infobox,
                        'entity':       gene.title
                    })
                # Previous stable version
                block_version = GeneBlockInfoboxVersion.objects.filter(is_stable=True,version_status='active', is_disabled=False, gene_id=entity_id).order_by('-created_at')[:1]
                if block_version:
                    for item in block_version:
                        infobox = []
                        block = GeneBlockInfobox.objects.filter(gene_block_version_id=item.id)
                        for i in block:
                            infobox.append({
                                'description':      i.description,
                                'chromosome':       i.chromosome,
                                'start':            i.start,
                                'end':              i.end,
                                'number_of_exons':  i.number_of_exons,
                                'protein_products': i.protein_products
                            })
                        gene = Gene.objects.get(pk=item.gene_id)
                        stable.append({
                            'timestamp':    item.created_at,
                            'title':        'Alias',
                            'page':         'Gene',
                            'kind':         'Gene - Infobox',
                            'infobox':      infobox,
                            'entity':       gene.title
                        })
        if block_gene.kind == 'general_publications':
            block_version = GeneBlockPublicationVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
            if block_version:
                for item in block_version:
                    entity_id = item.gene_id
                    pub = {}
                    pub['content'] = []
                    block = GeneBlockPublication.objects.filter(gene_block_version_id=item.id)
                    if block:
                        for i in block:
                            html = '<tr>'
                            html += '<td>' + i.pmid + '</td>'
                            html += '<td>' + i.doi + '</td>'
                            html += '<td>' + i.pmc + '</td>'
                            html += '<td>' + i.title + '</td>'
                            html += '<td>' + i.authors + '</td>'
                            html += '<td>' + i.journal + '</td>'
                            html += '</tr>'
                            pub['content'].append(html)
                        pub['header'] = ['pmid', 'doi', 'pmc', 'title', 'authors', 'journal']
                    gene = Gene.objects.get(pk=item.gene_id)
                    records.append({
                        'id':           item.id,
                        'timestamp':    item.created_at,
                        'title':        'Alias',
                        'page':         'Gene',
                        'kind':         'General - Publication',
                        'publication':  pub,
                        'entity':       gene.title
                    })
                # Previous stable version
                block_version = GeneBlockPublicationVersion.objects.filter(is_stable=True, version_status='Active', is_disabled=False, gene_id=entity_id).order_by('-created_at')[:1]
                if block_version:
                    for item in block_version:
                        pub = {}
                        pub['content'] = []
                        block = GeneBlockPublication.objects.filter(gene_block_version_id=item.id)
                        if block:
                            for i in block:
                                html = '<tr>'
                                html += '<td>' + i.pmid + '</td>'
                                html += '<td>' + i.doi + '</td>'
                                html += '<td>' + i.pmc + '</td>'
                                html += '<td>' + i.title + '</td>'
                                html += '<td>' + i.authors + '</td>'
                                html += '<td>' + i.journal + '</td>'
                                html += '</tr>'
                                pub['content'].append(html)
                            pub['header'] = ['pmid', 'doi', 'pmc', 'title', 'authors', 'journal']
                        gene = Gene.objects.get(pk=item.gene_id)
                        stable.append({
                            'timestamp':    item.created_at,
                            'title':        'Alias',
                            'page':         'Gene',
                            'kind':         'General - Publication',
                            'publication':  pub,
                            'entity':       gene.title
                        })
        return {
            'records': records,
            'stable': stable
        }
class GetBlockValidationVariation(handlers.standard.GetHandler):
    def get_data(self, data):
        records = []
        stable = []
        entity_id = ''
        block_variation = VariationBlock.objects.get(pk=data['id'])
        block_version = VariationBlockVersion.objects.filter(is_stable=False, is_disabled=False, variation_block_id=data['id'])[:1]
        if block_variation.kind == 'general_text':
            if block_version:
                for item in block_version:
                    entity_id = item.variation_id
                    block = VariationBlock.objects.get(pk=item.variation_block_id)
                    variation = Variation.objects.get(pk=item.variation_id)
                    records.append({
                        'id':           item.id,
                        'timestamp':    item.created_at,
                        'title':        item.title,
                        'page':         'Variation',
                        'kind':         'General - Text',
                        'text':         item.text,
                        'entity':       variation.title
                    })
                # Previous stable version
                block_version = VariationBlockVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, variation_block_id=data['id'], variation_id=entity_id).order_by('-created_at')[:1]
                if block_version:
                    for item in block_version:
                        block = VariationBlock.objects.get(pk=item.variation_block_id)
                        variation = Variation.objects.get(pk=item.variation_id)
                        stable.append({
                            'timestamp':    item.created_at,
                            'title':        item.title,
                            'page':         'Variation',
                            'kind':         'General - Text',
                            'text':         item.text,
                            'entity':       variation.title
                        })
        if block_variation.kind == 'general_alias':
            block_version = VariationBlockAliasVersion.objects.filter(is_stable=False, is_disabled=False, variation_block_id=data['id'])[:1]
            if block_version:
                for item in block_version:
                    entity_id = item.variation_id
                    alias = []
                    block = VariationBlockAlias.objects.filter(variation_block_version_id=item.id)
                    for i in block:
                        alias.append(i.alias)
                    variation = Variation.objects.get(pk=item.variation_id)
                    records.append({
                        'id':           item.id,
                        'timestamp':    item.created_at,
                        'title':        'Alias',
                        'page':         'Variation',
                        'kind':         'General - Alias',
                        'alias':         alias,
                        'entity':       variation.title
                    })
                # Previous stable version
                block_version = VariationBlockAliasVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, variation_block_id=data['id'], variation_id=entity_id).order_by('-created_at')[:1]
                if block_version:
                    for item in block_version:
                        alias = []
                        block = VariationBlockAlias.objects.filter(variation_block_version_id=item.id)
                        for i in block:
                            alias.append(i.alias)
                        variation = Variation.objects.get(pk=item.variation_id)
                        stable.append({
                            'timestamp':    item.created_at,
                            'title':        'Alias',
                            'page':         'Variation',
                            'kind':         'General - Alias',
                            'alias':         alias,
                            'entity':       variation.title
                        })
        if block_variation.kind == 'variation_effect':
            block_version = VariationBlockEffectVersion.objects.filter(is_stable=False, is_disabled=False, variation_block_id=data['id'])[:1]
            if block_version:
                for item in block_version:
                    entity_id = item.variation_id
                    effects = {}
                    block = VariationBlockEffect.objects.filter(variation_block_version_id=item.id)
                    if block:
                        effects['content'] = []
                        for i in block:
                            html = '<tr>'
                            html += '<td>' + i.popcode + '</td>'
                            html += '<td>' + i.genotype + '</td>'
                            html += '<td>' + i.risk + '</td>'
                            html += '<td>' + str(i.odd_ratio) + '</td>'
                            html += '<td>' + i.evidences + '</td>'
                            html += '<td>' + i.pmid + '</td>'
                            html += '</tr>'
                            effects['content'].append(html)

                        effects['header'] = ['popcode', 'genotype', 'risk', 'odd_ratio', 'evidences', 'pmid']

                    variation = Variation.objects.get(pk=item.variation_id)
                    records.append({
                        'id':           item.id,
                        'timestamp':    item.created_at,
                        'title':        'Alias',
                        'page':         'Variation',
                        'kind':         'Variation - Effects',
                        'effects':      effects,
                        'entity':       variation.title
                    })

                # Previous stable version
                block_version = VariationBlockEffectVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, variation_block_id=data['id'], variation_id=entity_id).order_by('-created_at')[:1]

                if block_version:
                    for item in block_version:
                        effects = {}
                        block = VariationBlockEffect.objects.filter(variation_block_version_id=item.id)
                        if block:
                            effects['content'] = []
                            for i in block:
                                html = '<tr>'
                                html += '<td>' + i.popcode + '</td>'
                                html += '<td>' + i.genotype + '</td>'
                                html += '<td>' + i.risk + '</td>'
                                html += '<td>' + str(i.odd_ratio) + '</td>'
                                html += '<td>' + i.evidences + '</td>'
                                html += '<td>' + i.pmid + '</td>'
                                html += '</tr>'
                                effects['content'].append(html)
                            effects['header'] = ['popcode', 'genotype', 'risk', 'odd_ratio', 'evidences', 'pmid']
                        variation = Variation.objects.get(pk=item.variation_id)
                        stable.append({
                            'timestamp':    item.created_at,
                            'title':        'Alias',
                            'page':         'Variation',
                            'kind':         'Variation - Effects',
                            'effects':      effects,
                            'entity':       variation.title
                        })
        if block_variation.kind == 'variation_frequency':
            block_version = VariationBlockFrequencyVersion.objects.filter(is_stable=False, is_disabled=False, variation_block_id=data['id'])[:1]
            if block_version:
                for item in block_version:
                    entity_id = item.variation_id
                    frequencies = []
                    block = VariationBlockFrequency.objects.filter(variation_block_version_id=item.id)
                    for i in block:
                        frequencies.append({
                            'popcode':              i.popcode,
                            'genotype_count_00':    i.genotype_count_00,
                            'genotype_count_01':    i.genotype_count_01,
                            'genotype_count_11':    i.genotype_count_11
                        })
                    variation = Variation.objects.get(pk=item.variation_id)
                    records.append({
                        'id':           item.id,
                        'timestamp':    item.created_at,
                        'title':        'Alias',
                        'page':         'Variation',
                        'kind':         'Variation - Frequency',
                        'frequencies':  frequencies,
                        'entity':       variation.title
                    })
                # Previous stable version
                block_version = VariationBlockFrequencyVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, variation_block_id=data['id'], variation_id=entity_id).order_by('-created_at')[:1]
                if block_version:
                    for item in block_version:
                        frequencies = []
                        block = VariationBlockFrequency.objects.filter(variation_block_version_id=item.id)
                        for i in block:
                            frequencies.append({
                                'popcode':              i.popcode,
                                'genotype_count_00':    i.genotype_count_00,
                                'genotype_count_01':    i.genotype_count_01,
                                'genotype_count_11':    i.genotype_count_11
                            })
                        variation = Variation.objects.get(pk=item.variation_id)
                        stable.append({
                            'timestamp':    item.created_at,
                            'title':        'Alias',
                            'page':         'Variation',
                            'kind':         'Variation - Frequency',
                            'frequencies':  frequencies,
                            'entity':       variation.title
                        })
        if block_variation.kind == 'variation_infobox':
            block_version = VariationBlockInfoboxVersion.objects.filter(is_stable=False, is_disabled=False, variation_block_id=data['id'])[:1]
            if block_version:
                for item in block_version:
                    entity_id = item.variation_id
                    infobox = []
                    block = VariationBlockInfobox.objects.filter(variation_block_version_id=item.id)
                    for i in block:
                        infobox.append({
                            i.key:    i.value
                        })
                    variation = Variation.objects.get(pk=item.variation_id)
                    records.append({
                        'id':           item.id,
                        'timestamp':    item.created_at,
                        'title':        'Alias',
                        'page':         'Variation',
                        'kind':         'Variation - Infobox',
                        'infobox':      infobox,
                        'entity':       variation.title
                    })
                # Previous stable version
                block_version = VariationBlockInfoboxVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, variation_block_id=data['id'], variation_id=entity_id).order_by('-created_at')[:1]
                if block_version:
                    for item in block_version:
                        infobox = []
                        block = VariationBlockInfobox.objects.filter(variation_block_version_id=item.id)
                        for i in block:
                            infobox.append({
                                i.key:    i.value
                            })
                        variation = Variation.objects.get(pk=item.variation_id)
                        stable.append({
                            'timestamp':    item.created_at,
                            'title':        'Alias',
                            'page':         'Variation',
                            'kind':         'Variation - Infobox',
                            'infobox':      infobox,
                            'entity':       variation.title
                        })
        if block_variation.kind == 'general_publications':
            block_version = VariationBlockPublicationVersion.objects.filter(is_stable=False, is_disabled=False, variation_block_id=data['id'])[:1]
            if block_version:
                for item in block_version:
                    entity_id = item.variation_id
                    pub = {}
                    pub['content'] = []
                    block = VariationBlockPublication.objects.filter(variation_block_version_id=item.id)
                    if block:
                        for i in block:
                            html = '<tr>'
                            html += '<td>' + i.pmid + '</td>'
                            html += '<td>' + i.doi + '</td>'
                            html += '<td>' + i.pmc + '</td>'
                            html += '<td>' + i.title + '</td>'
                            html += '<td>' + i.authors + '</td>'
                            html += '<td>' + i.journal + '</td>'
                            html += '</tr>'
                            pub['content'].append(html)
                        pub['header'] = ['pmid', 'doi', 'pmc', 'title', 'authors', 'journal']
                    variation = Variation.objects.get(pk=item.variation_id)
                    records.append({
                        'id':           item.id,
                        'timestamp':    item.created_at,
                        'title':        'Alias',
                        'page':         'Variation',
                        'kind':         'General - Publication',
                        'publication':  pub,
                        'entity':       variation.title
                    })
                # Previous stable version
                block_version = VariationBlockPublicationVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, variation_block_id=data['id'], variation_id=entity_id).order_by('-created_at')[:1]
                if block_version:
                    for item in block_version:
                        pub = {}
                        pub['content'] = []
                        block = VariationBlockPublication.objects.filter(variation_block_version_id=item.id)
                        if block:
                            for i in block:
                                html = '<tr>'
                                html += '<td>' + i.pmid + '</td>'
                                html += '<td>' + i.doi + '</td>'
                                html += '<td>' + i.pmc + '</td>'
                                html += '<td>' + i.title + '</td>'
                                html += '<td>' + i.authors + '</td>'
                                html += '<td>' + i.journal + '</td>'
                                html += '</tr>'
                                pub['content'].append(html)
                            pub['header'] = ['pmid', 'doi', 'pmc', 'title', 'authors', 'journal']
                        variation = Variation.objects.get(pk=item.variation_id)
                        stable.append({
                            'timestamp':    item.created_at,
                            'title':        'Alias',
                            'page':         'Variation',
                            'kind':         'General - Publication',
                            'publication':  pub,
                            'entity':       variation.title
                        })
        return {
            'records': records,
            'stable': stable
        }

class GetBlockValidationDisease(handlers.standard.GetHandler):
    def get_data(self, data):
        records = []
        stable = []
        entity_id = ''
        block_disease = DiseaseBlock.objects.get(pk=data['id'])
        if block_disease.kind == 'general_text':
            if not records:
                block_version = DiseaseBlockVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
                if block_version:
                    for item in block_version:
                        entity_id = item.disease_id
                        block = DiseaseBlock.objects.get(pk=item.disease_block_id)
                        disease = Disease.objects.get(pk=item.disease_id)
                        records.append({
                            'id':           item.id,
                            'timestamp':    item.created_at,
                            'title':        item.title,
                            'page':         'Disease',
                            'kind':         'General - Text',
                            'text':         item.text,
                            'entity':       disease.title
                        })
                    # Previous stable version
                    block_version = DiseaseBlockVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, disease_id=entity_id).order_by('-created_at')[:1]
                    if block_version:
                        for item in block_version:
                            block = DiseaseBlock.objects.get(pk=item.disease_block_id)
                            disease = Disease.objects.get(pk=item.disease_id)
                            stable.append({
                                'timestamp':    item.created_at,
                                'title':        item.title,
                                'page':         'Disease',
                                'kind':         'General - Text',
                                'text':         item.text,
                                'entity':       disease.title
                            })
        if block_disease.kind == 'general_alias':
            block_version = DiseaseBlockAliasVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
            if block_version:
                for item in block_version:
                    entity_id = item.disease_id
                    alias = []
                    block = DiseaseBlockAlias.objects.filter(disease_block_version_id=item.id)
                    for i in block:
                        alias.append(i.alias)
                    disease = Disease.objects.get(pk=item.disease_id)
                    records.append({
                        'id':           item.id,
                        'timestamp':    item.created_at,
                        'title':        'Alias',
                        'page':         'Disease',
                        'kind':         'General - Alias',
                        'alias':         alias,
                        'entity':        disease.title
                    })
                # Previous stable version
                block_version = DiseaseBlockAliasVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, disease_id=entity_id).order_by('-created_at')[:1]
                if block_version:
                    for item in block_version:
                        alias = []
                        block = DiseaseBlockAlias.objects.filter(disease_block_version_id=item.id)
                        for i in block:
                            alias.append(i.alias)
                        disease = Disease.objects.get(pk=item.disease_id)
                        stable.append({
                            'timestamp':    item.created_at,
                            'title':        'Alias',
                            'page':         'Disease',
                            'kind':         'General - Alias',
                            'alias':         alias,
                            'entity':        disease.title
                        })
        if block_disease.kind == 'general_publications':
            block_version = DiseaseBlockPublicationVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
            if block_version:
                for item in block_version:
                    entity_id = item.disease_id
                    pub = {}
                    pub['content'] = []
                    block = DiseaseBlockPublication.objects.filter(disease_block_version_id=item.id)
                    if block:
                        for i in block:
                            html = '<tr>'
                            html += '<td>' + i.pmid + '</td>'
                            html += '<td>' + i.doi + '</td>'
                            html += '<td>' + i.pmc + '</td>'
                            html += '<td>' + i.title + '</td>'
                            html += '<td>' + i.authors + '</td>'
                            html += '<td>' + i.journal + '</td>'
                            html += '</tr>'
                            pub['content'].append(html)
                        pub['header'] = ['pmid', 'doi', 'pmc', 'title', 'authors', 'journal']
                    disease = Disease.objects.get(pk=item.disease_id)
                    records.append({
                        'id':           item.id,
                        'timestamp':    item.created_at,
                        'title':        'Alias',
                        'page':         'Disease',
                        'kind':         'General - Publication',
                        'publication':  pub,
                        'entity':       disease.title
                    })
                # Previous stable version
                block_version = DiseaseBlockPublicationVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, disease_id=entity_id).order_by('-created_at')[:1]
                if block_version:
                    for item in block_version:
                        pub = {}
                        pub['content'] = []
                        block = DiseaseBlockPublication.objects.filter(disease_block_version_id=item.id)
                        if block:
                            for i in block:
                                html = '<tr>'
                                html += '<td>' + i.pmid + '</td>'
                                html += '<td>' + i.doi + '</td>'
                                html += '<td>' + i.pmc + '</td>'
                                html += '<td>' + i.title + '</td>'
                                html += '<td>' + i.authors + '</td>'
                                html += '<td>' + i.journal + '</td>'
                                html += '</tr>'
                                pub['content'].append(html)
                            pub['header'] = ['pmid', 'doi', 'pmc', 'title', 'authors', 'journal']
                        disease = Disease.objects.get(pk=item.disease_id)
                        stable.append({
                            'timestamp':    item.created_at,
                            'title':        'Alias',
                            'page':         'Disease',
                            'kind':         'General - Publication',
                            'publication':  pub,
                            'entity':       disease.title
                        })
        return {
            'records': records,
            'stable': stable
        }

class GetBlockValidationTrait(handlers.standard.GetHandler):
    def get_data(self, data):
        records = []
        stable = []
        entity_id = ''
        block_trait = TraitBlock.objects.get(pk=data['id'])
        if block_trait.kind == 'general_text':
            block_version = TraitBlockVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
            if block_version:
                for item in block_version:
                    entity_id = item.trait_id
                    block = TraitBlock.objects.get(pk=item.trait_block_id)
                    trait = Trait.objects.get(pk=item.trait_id)
                    records.append({
                        'id':           item.id,
                        'timestamp':    item.created_at,
                        'title':        item.title,
                        'page':         'Trait',
                        'kind':         'General - Text',
                        'text':         item.text,
                        'entity':       trait.title
                    })
                # Previous stable version
                block_version = TraitBlockVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, trait_id=entity_id).order_by('-created_at')[:1]
                if block_version:
                    for item in block_version:
                        block = TraitBlock.objects.get(pk=item.trait_block_id)
                        trait = Trait.objects.get(pk=item.trait_id)
                        stable.append({
                            'timestamp':    item.created_at,
                            'title':        item.title,
                            'page':         'Trait',
                            'kind':         'General - Text',
                            'text':         item.text,
                            'entity':       trait.title
                        })
        if block_trait.kind == 'general_alias':
            block_version = TraitBlockAliasVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
            if block_version:
                for item in block_version:
                    entity_id = item.trait_id
                    alias = []
                    block = TraitBlockAlias.objects.filter(trait_block_version_id=item.id)
                    for i in block:
                        alias.append(i.alias)
                    trait = Trait.objects.get(pk=item.trait_id)
                    records.append({
                        'id':           item.id,
                        'timestamp':    item.created_at,
                        'title':        'Alias',
                        'page':         'Trait',
                        'kind':         'General - Alias',
                        'alias':         alias,
                        'entity':        trait.title
                    })
                # Previous stable version
                block_version = TraitBlockAliasVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, trait_id=entity_id).order_by('-created_at')[:1]
                if block_version:
                    for item in block_version:
                        alias = []
                        block = TraitBlockAlias.objects.filter(trait_block_version_id=item.id)
                        for i in block:
                            alias.append(i.alias)
                        trait = Trait.objects.get(pk=item.trait_id)
                        stable.append({
                            'timestamp':    item.created_at,
                            'title':        'Alias',
                            'page':         'Trait',
                            'kind':         'General - Alias',
                            'alias':         alias,
                            'entity':        trait.title
                        })
        if block_trait.kind == 'general_publications':
            block_version = TraitBlockPublicationVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
            if block_version:
                for item in block_version:
                    entity_id = item.trait_id
                    pub = {}
                    pub['content'] = []
                    block = TraitBlockPublication.objects.filter(trait_block_version_id=item.id)
                    if block:
                        for i in block:
                            html = '<tr>'
                            html += '<td>' + i.pmid + '</td>'
                            html += '<td>' + i.doi + '</td>'
                            html += '<td>' + i.pmc + '</td>'
                            html += '<td>' + i.title + '</td>'
                            html += '<td>' + i.authors + '</td>'
                            html += '<td>' + i.journal + '</td>'
                            html += '</tr>'
                            pub['content'].append(html)
                        pub['header'] = ['pmid', 'doi', 'pmc', 'title', 'authors', 'journal']
                    trait = Trait.objects.get(pk=item.trait_id)
                    records.append({
                        'id':           item.id,
                        'timestamp':    item.created_at,
                        'title':        'Publication',
                        'page':         'Trait',
                        'kind':         'General - Publication',
                        'publication':  pub,
                        'entity':       trait.title
                    })
                # Previous stable version
                block_version = TraitBlockPublicationVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, trait_id=entity_id).order_by('-created_at')[:1]
                if block_version:
                    for item in block_version:
                        pub = {}
                        pub['content'] = []
                        block = TraitBlockPublication.objects.filter(trait_block_version_id=item.id)
                        if block:
                            for i in block:
                                html = '<tr>'
                                html += '<td>' + i.pmid + '</td>'
                                html += '<td>' + i.doi + '</td>'
                                html += '<td>' + i.pmc + '</td>'
                                html += '<td>' + i.title + '</td>'
                                html += '<td>' + i.authors + '</td>'
                                html += '<td>' + i.journal + '</td>'
                                html += '</tr>'
                                pub['content'].append(html)
                            pub['header'] = ['pmid', 'doi', 'pmc', 'title', 'authors', 'journal']
                        trait = Trait.objects.get(pk=item.trait_id)
                        stable.append({
                            'timestamp':    item.created_at,
                            'title':        'Publication',
                            'page':         'Trait',
                            'kind':         'General - Publication',
                            'publication':  pub,
                            'entity':       trait.title
                        })
        return {
            'records': records,
            'stable': stable
        }

class GetBlockValidationTreatment(handlers.standard.GetHandler):
    def get_data(self, data):
        records = []
        stable = []
        entity_id = ''
        block_treatment = TreatmentBlock.objects.get(pk=data['id'])
        if block_treatment.kind == 'general_text':
            block_version = TreatmentBlockVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
            if block_version:
                for item in block_version:
                    entity_id = item.treatment_id
                    block = TreatmentBlock.objects.get(pk=item.treatment_block_id)
                    treatment = Treatment.objects.get(pk=item.treatment_id)
                    records.append({
                        'id':           item.id,
                        'timestamp':    item.created_at,
                        'title':        item.title,
                        'page':         'Treatment',
                        'kind':         'General - Text',
                        'text':         item.text,
                        'entity':       treatment.title
                    })
                # Previous stable version
                block_version = TreatmentBlockVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, treatment_id=entity_id).order_by('-created_at')[:1]
                if block_version:
                    for item in block_version:
                        block = TreatmentBlock.objects.get(pk=item.treatment_block_id)
                        treatment = Treatment.objects.get(pk=item.treatment_id)
                        stable.append({
                            'timestamp':    item.created_at,
                            'title':        item.title,
                            'page':         'Treatment',
                            'kind':         'General - Text',
                            'text':         item.text,
                            'entity':       treatment.title
                        })
        if block_treatment.kind == 'general_alias':
            block_version = TreatmentBlockAliasVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
            if block_version:
                for item in block_version:
                    entity_id = item.treatment_id
                    alias = []
                    block = TreatmentBlockAlias.objects.filter(treatment_block_version_id=item.id)
                    for i in block:
                        alias.append(i.alias)
                    treatment = Treatment.objects.get(pk=item.treatment_id)
                    records.append({
                        'id':           item.id,
                        'timestamp':    item.created_at,
                        'title':        'Alias',
                        'page':         'Treatment',
                        'kind':         'General - Alias',
                        'alias':         alias,
                        'entity':        treatment.title
                    })
                # Previous stable version
                block_version = TreatmentBlockAliasVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, treatment_id=entity_id).order_by('-created_at')[:1]
                if block_version:
                    for item in block_version:
                        alias = []
                        block = TreatmentBlockAlias.objects.filter(treatment_block_version_id=item.id)
                        for i in block:
                            alias.append(i.alias)
                        treatment = Treatment.objects.get(pk=item.treatment_id)
                        stable.append({
                            'timestamp':    item.created_at,
                            'title':        'Alias',
                            'page':         'Treatment',
                            'kind':         'General - Alias',
                            'alias':         alias,
                            'entity':        treatment.title
                        })
        if block_treatment.kind == 'general_publications':

            block_version = TreatmentBlockPublicationVersion.objects.filter(is_stable=False, is_disabled=False)[:1]
            if block_version:
                for item in block_version:
                    entity_id = item.treatment_id
                    pub = {}
                    pub['content'] = []
                    block = TreatmentBlockPublication.objects.filter(treatment_block_version_id=item.id)
                    if block:
                        for i in block:
                            html = '<tr>'
                            html += '<td>' + i.pmid + '</td>'
                            html += '<td>' + i.doi + '</td>'
                            html += '<td>' + i.pmc + '</td>'
                            html += '<td>' + i.title + '</td>'
                            html += '<td>' + i.authors + '</td>'
                            html += '<td>' + i.journal + '</td>'
                            html += '</tr>'
                            pub['content'].append(html)
                        pub['header'] = ['pmid', 'doi', 'pmc', 'title', 'authors', 'journal']
                    treatment = Treatment.objects.get(pk=item.treatment_id)
                    records.append({
                        'id':           item.id,
                        'timestamp':    item.created_at,
                        'title':        'Alias',
                        'page':         'Treatment',
                        'kind':         'General - Publication',
                        'publication':  pub,
                        'entity':       treatment.title
                    })
                # Previous stable version
                block_version = TreatmentBlockPublicationVersion.objects.filter(is_stable=True, version_status='active', is_disabled=False, treatment_id=entity_id).order_by('-created_at')[:1]
                if block_version:
                    for item in block_version:
                        pub = {}
                        pub['content'] = []
                        block = TreatmentBlockPublication.objects.filter(treatment_block_version_id=item.id)
                        if block:
                            for i in block:
                                html = '<tr>'
                                html += '<td>' + i.pmid + '</td>'
                                html += '<td>' + i.doi + '</td>'
                                html += '<td>' + i.pmc + '</td>'
                                html += '<td>' + i.title + '</td>'
                                html += '<td>' + i.authors + '</td>'
                                html += '<td>' + i.journal + '</td>'
                                html += '</tr>'
                                pub['content'].append(html)
                            pub['header'] = ['pmid', 'doi', 'pmc', 'title', 'authors', 'journal']
                        treatment = Treatment.objects.get(pk=item.treatment_id)
                        stable.append({
                            'timestamp':    item.created_at,
                            'title':        'Alias',
                            'page':         'Treatment',
                            'kind':         'General - Publication',
                            'publication':  pub,
                            'entity':       treatment.title
                        })
        return {
            'records': records,
            'stable': stable
        }
class BlockStableUpdate(handlers.standard.DeleteHandler):
    def delete(self, data):
        block_version = ''
        if data['params']['page'] == 'Variation':
            if data['params']['kind'].strip("\s") == 'General - Text'.strip("\s"):
                block_version = VariationBlockVersion.objects.get(pk=data['params']['id'])
            elif data['params']['kind'].strip("\s") == 'General - Alias'.strip("\s"):
                block_version = VariationBlockAliasVersion.objects.get(pk=data['params']['id'])
            elif data['params']['kind'].strip("\s") == 'General - Publication'.strip("\s"):
                block_version = VariationBlockPublicationVersion.objects.get(pk=data['params']['id'])
            elif data['params']['kind'].strip("\s") == 'Variation - Infobox'.strip("\s"):
                block_version = VariationBlockInfoboxVersion.objects.get(pk=data['params']['id'])
            elif data['params']['kind'].strip("\s") == 'Variation - Effect'.strip("\s"):
                block_version = VariationBlockEffectVersion.objects.get(pk=data['params']['id'])
            elif data['params']['kind'].strip("\s") == 'Variation - Frequency'.strip("\s"):
                block_version = VariationBlockFrequencyVersion.objects.get(pk=data['params']['id'])
            elif data['params']['kind'].strip("\s") == 'Variation - Publication text'.strip("\s"):
                block_version = VariationBlockPublicationTextVersion.objects.get(pk=data['params']['id'])
            elif data['params']['kind'].strip("\s") == 'General - Disgenet diseases'.strip("\s"):
                block_version = VariationBlockDisgenetDiseasesVersion.objects.get(pk=data['params']['id'])        
        elif data['params']['page'] == 'Disease':
            if data['params']['kind'].strip("\s") == 'General - Text'.strip("\s"):
                block_version = DiseaseBlockVersion.objects.get(pk=data['params']['id'])
            elif data['params']['kind'].strip("\s") == 'General - Alias'.strip("\s"):
                block_version = DiseaseBlockAliasVersion.objects.get(pk=data['params']['id'])
            elif data['params']['kind'].strip("\s") == 'General - Publication'.strip("\s"):
                block_version = DiseaseBlockPublicationVersion.objects.get(pk=data['params']['id'])
        elif data['params']['page'] == 'Gene':
            if data['params']['kind'].strip("\s") == 'General - Text'.strip("\s"):
                block_version = GeneBlockVersion.objects.get(pk=data['params']['id'])
            elif data['params']['kind'].strip("\s") == 'General - Alias'.strip("\s"):
                block_version = GeneBlockAliasVersion.objects.get(pk=data['params']['id'])
            elif data['params']['kind'].strip("\s") == 'General - Publication'.strip("\s"):
                block_version = GeneBlockPublicationVersion.objects.get(pk=data['params']['id'])
            elif data['params']['kind'].strip("\s") == 'Gene - Infobox'.strip("\s"):
                block_version = GeneBlockInfoboxVersion.objects.get(pk=data['params']['id'])
            elif data['params']['kind'].strip("\s") == 'Gene - Effect'.strip("\s"):
                block_version = GeneBlockEffectVersion.objects.get(pk=data['params']['id'])
        elif data['params']['page'] == 'Trait':
            if data['params']['kind'].strip("\s") == 'General - Text'.strip("\s"):
                block_version = TraitBlockVersion.objects.get(pk=data['params']['id'])
            elif data['params']['kind'].strip("\s") == 'General - Alias'.strip("\s"):
                block_version = TraitBlockAliasVersion.objects.get(pk=data['params']['id'])
            elif data['params']['kind'].strip("\s") == 'General - Publication'.strip("\s"):
                block_version = TraitBlockPublicationVersion.objects.get(pk=data['params']['id'])
        elif data['params']['page'] == 'Treatment':
            if data['params']['kind'].strip("\s") == 'General - Text'.strip("\s"):
                block_version = TreatmentBlockVersion.objects.get(pk=data['params']['id'])
            elif data['params']['kind'].strip("\s") == 'General - Alias'.strip("\s"):
                block_version = TreatmentBlockAliasVersion.objects.get(pk=data['params']['id'])
            elif data['params']['kind'].strip("\s") == 'General - Publication'.strip("\s"):
                block_version = TreatmentBlockPublicationVersion.objects.get(pk=data['params']['id'])
        block_version.version_status = data['params']['version_status']
        block_version.is_stable = True
        block_version.save()
        return 1
