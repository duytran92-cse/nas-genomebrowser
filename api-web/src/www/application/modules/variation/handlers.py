from notasquare.urad_api import *
from application.models import *
from application import constants
from application.modules.variation import components
from application.modules.variation_block import components as block_components
import ast

class List(handlers.standard.ListHandler):
    def create_query(self, data):
        query = Variation.objects
        query = query.filter(is_disabled=False)
        if 'text' in data:
            query = query.filter(title__contains=data['text'])
        if 'rs_filter' in data:
            query = query.filter(title__in=ast.literal_eval(data['rs_filter']))
        if 'isGene' in data:
            query = query.filter(num_associated_gene__gte = 1)
        if 'isDisease' in data:
            query = query.filter(num_associated_disease__gte = 1)
        if 'isPub' in data:
            query = query.filter(num_associated_publication__gte = 1)
        return query
    def serialize_entry(self, data):
        helper = components.DataHelper()
        return {
            'id':                           data.id,
            'title':                        data.title,
            'associated_genes':             helper.load_associated_genes(data.id),
            'associated_diseases':          helper.load_associated_diseases(data.id),
            'associated_diseases_group_name':          helper.load_associated_diseases_group_name(data.id),
            'associated_publications':      helper.load_associated_publications(data.id),
            'genotypes':                    helper.load_genotypes(data.id),
        }

class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        result = {}
        helper = components.DataHelper()
        variation = Variation.objects.get(pk=data['id'])
        result['id']      = variation.id
        result['title']   = variation.title
        result['associated_genes']        = helper.load_associated_genes(data['id'])
        result['associated_diseases']     = helper.load_associated_diseases(data['id'])
        result['associated_publications'] = helper.load_associated_publications(data['id'])
        result['genotypes'] = helper.load_genotypes(data['id'])
        return result

class View(handlers.standard.GetHandler):
    def get_data(self, data):
        result = {}
        block_helper = block_components.VariationBlockHelper()
        helper = components.DataHelper()
        variation = Variation.objects.get(title=data['id'])
        blocks = { 'main': [], 'left': [],'right': []}
        rows = VariationBlock.objects.filter(variation_id=variation.id, is_disabled = False).order_by('-sort_order').all()
        if 'filter' in data:
            filter_val = data.get('filter', 'Global')
        else:
            filter_val = 'None'
        for r in rows:
            block = block_helper.load_variation_block(r.id, filter_val)
            blocks[r.position].append(block)
        result['id']      = variation.id
        result['title']   = variation.title
        result['blocks']  = blocks
        result['genotypes'] = helper.load_genotypes(variation.id)
        return result

class Create(handlers.standard.CreateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('title', 'string'):
            self.add_error('title', 'MUST_NOT_BE_EMPTY')
        return parser.get_data()
    def create(self, data):
        variation = Variation()
        variation.title = data['title']
        variation.save()
        # Save extra info
        VariationAssociatedGene.objects.filter(variation_id=variation.id).delete()
        for gene in data['associated_genes']:
            variation_ass_gene = VariationAssociatedGene()
            variation_ass_gene.gene_name = gene['gene_name']
            variation_ass_gene.variation_id = variation.id
            variation_ass_gene.save()

        VariationGenotype.objects.filter(variation_id=variation.id).delete()
        for genotype in data['genotypes']:
            variation_genotype = VariationGenotype()
            variation_genotype.genotype = genotype['genotype_eff']
            variation_genotype.box_color = genotype['box_color']
            variation_genotype.variation_id = variation.id
            variation_genotype.source = 'http://www.ensembl.org/index.html'
            variation_genotype.save()

        VariationAssociatedPublication.objects.filter(variation_id=variation.id).delete()
        for publication in data['associated_publications']:
            variation_ass_publication = VariationAssociatedPublication()
            variation_ass_publication.variation_id = variation.id
            variation_ass_publication.pmid = publication['pmid']
            variation_ass_publication.doi = publication['doi']
            variation_ass_publication.pmc = publication['pmc']
            variation_ass_publication.title = publication['title']
            variation_ass_publication.authors = publication['authors']
            variation_ass_publication.journal = publication['journal']
            variation_ass_publication.save()
        return variation

class Update(handlers.standard.UpdateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if 'title' in params:
            if not parser.parse('title', 'string'):
                self.add_error('title', 'MUST_NOT_BE_EMPTY')
        return parser.get_data()
    def update(self, data):
        variation = Variation.objects.get(pk=data['id'])
        if 'title' in data:
            variation.title = data['title']
        variation.save()
        # Save extra info
        VariationAssociatedGene.objects.filter(variation_id=variation.id).delete()
        for gene in data['associated_genes']:
            variation_ass_gene = VariationAssociatedGene()
            variation_ass_gene.gene_name = gene['gene_name']
            variation_ass_gene.variation_id = variation.id
            variation_ass_gene.save()

        VariationAssociatedDisease.objects.filter(variation_id=variation.id).delete()
        for disease in data['associated_diseases']:
            variation_ass_disease = VariationAssociatedDisease()
            variation_ass_disease.disease_name = disease['disease_name']
            variation_ass_disease.variation_id = variation.id
            variation_ass_disease.save()

        VariationAssociatedPublication.objects.filter(variation_id=variation.id).delete()
        for publication in data['associated_publications']:
            variation_ass_publication = VariationAssociatedPublication()
            variation_ass_publication.variation_id = variation.id
            variation_ass_publication.pmid = publication['pmid']
            variation_ass_publication.doi = publication['doi']
            variation_ass_publication.pmc = publication['pmc']
            variation_ass_publication.title = publication['title']
            variation_ass_publication.authors = publication['authors']
            variation_ass_publication.journal = publication['journal']
            variation_ass_publication.save()

        VariationGenotype.objects.filter(variation_id=variation.id).delete()
        for genotype in data['genotypes']:
            variation_genotype = VariationGenotype()
            variation_genotype.genotype = genotype['genotype_eff']
            variation_genotype.box_color = genotype['box_color']
            variation_genotype.source = 'http://www.ensembl.org/index.html'
            variation_genotype.variation_id = variation.id
            variation_genotype.save()
        return variation


class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        variation = Variation.objects.get(pk=data['id'])
        variation.is_disabled = True
        variation.save()
        return 1

class Summary(handlers.standard.GetHandler):
    def get_data(self, data):

        result = []
        blocks = []
        comments = []
        active_blocks_version = []
        inactive_blocks_version = []

        variation = Variation.objects.get(pk=data['variation_id'])

        variation_genes = VariationAssociatedGene.objects.filter(variation_id=data['variation_id'])
        variation_gene = '111'

        if variation_genes:
            for item in variation_genes:
                variation_gene += ', ' + item.gene_name
        variation_gene = variation_gene.replace('111,','')

        variation_pubs = VariationAssociatedPublication.objects.filter(variation_id=data['variation_id'])
        variation_pub = []
        if variation_pubs:
            for item in variation_pubs:
                variation_pub.append('https://www.ncbi.nlm.nih.gov/pubmed/%s' % (item.pmid))
        variation_blocks = VariationBlock.objects.filter(variation_id=data['variation_id'],is_disabled=False)[:10]
        for item in variation_blocks:

            # Get active and latest version
            if item.kind == 'general_text':
                query = VariationBlockVersion.objects.filter(variation_block_id=item.id, version_status='active', is_disabled=False)
            elif item.kind == 'general_alias':
                query = VariationBlockAliasVersion.objects.filter(variation_block_id=item.id, version_status='active', is_disabled=False)
            elif item.kind == 'general_publications':
                query = VariationBlockPublicationVersion.objects.filter(variation_block_id=item.id, version_status='active', is_disabled=False)
            elif item.kind == 'variation_infobox':
                query = VariationBlockInfoboxVersion.objects.filter(variation_block_id=item.id, version_status='active', is_disabled=False)
            elif item.kind == 'variation_effect':
                query = VariationBlockEffectVersion.objects.filter(variation_block_id=item.id, version_status='active', is_disabled=False)
            elif item.kind == 'variation_frequency':
                query = VariationBlockFrequencyVersion.objects.filter(variation_block_id=item.id, version_status='active', is_disabled=False)
            elif item.kind == 'general_disgenet_diseases':
                query = VariationBlockDisgenetDiseasesVersion.objects.filter(variation_block_id=item.id, version_status='active', is_disabled=False)
            elif item.kind == 'variation_pub_text':
                query = VariationBlockPublicationTextVersion.objects.filter(variation_block_id=item.id, version_status='active', is_disabled=False)
            active_version = query.filter(is_stable=True).order_by('-created_at')[:1]
            latest_version = query.order_by('-created_at')[:1]
            l_ver = 0
            ac_ver = 0
            if latest_version.first():
                l_ver = latest_version.first().version

            if active_version.first():
                ac_ver = active_version.first().version
            blocks.append({
                'id': item.id,
                'kind': item.kind,
                'position': item.position,
                'title': item.title,
                'text': item.text,
                'sort_order': item.sort_order,
                'page_id': item.variation_id,
                'active_version': ac_ver,
                'latest_version': l_ver
            })
        total_blocks = VariationBlock.objects.filter(variation_id=data['variation_id'],is_disabled=False).count()

        active_blocks_versions = VariationBlockVersion.objects.filter(variation_id=data['variation_id'],is_disabled=False, version_status='active')[:10]
        for item in active_blocks_versions:
            block = VariationBlock.objects.get(pk=item.variation_block_id)
            active_blocks_version.append({
                'id': item.id,
                'title': item.title,
                'text': item.text,
                'author': item.author,
                'version': item.version,
                'page_id': item.variation_id,
                'page_block_id': item.variation_block_id,
                'kind': block.kind,
                'timestamp': item.created_at
            })
        total_active_blocks_version = VariationBlockVersion.objects.filter(variation_id=data['variation_id'],is_disabled=False, version_status='active').count()

        inactive_blocks_versions = VariationBlockVersion.objects.filter(variation_id=data['variation_id'],is_disabled=False, version_status='inactive')[:10]
        for item in inactive_blocks_versions:
            block = VariationBlock.objects.get(pk=item.variation_block_id)
            inactive_blocks_version.append({
                'id': item.id,
                'title': item.title,
                'text': item.text,
                'author': item.author,
                'version': item.version,
                'page_id': item.variation_id,
                'page_block_id': item.variation_block_id,
                'kind': block.kind,
                'timestamp': item.created_at
            })
        total_inactive_blocks_version = VariationBlockVersion.objects.filter(variation_id=data['variation_id'],is_disabled=False, version_status='inactive').count()

        variation_comment = Comment.objects.filter(page='variation',entity=variation.title)[:5]

        for item in variation_comment:
            user = User.objects.get(pk=item.user_id)
            comments.append({
                'id': item.id,
                'timestamp': item.timestamp,
                'user': user.name,
                'comment': item.comment,
                'page_id': data['variation_id']
            })
        total_comments = Comment.objects.filter(page='variation',entity=variation.title).count()

        result.append({
            'variation_id': data['variation_id'],
            'title': variation.title,
            'variation_gene': variation_gene,
            'variation_pub': variation_pub,
            'blocks': blocks,
            'total_blocks': total_blocks,
            'total_active_blocks_version': total_active_blocks_version,
            'active_blocks_version': active_blocks_version,
            'total_inactive_blocks_version': total_inactive_blocks_version,
            'inactive_blocks_version': inactive_blocks_version,
            'total_comments': total_comments,
            'comments': comments,
            'validation': 'variation'
        })

        return (result)

class GetGenotype(handlers.standard.ListHandler):
    def create_query(self, data):
        query = VariationGenotype.objects
        query = query.filter(variation_id=data['id'])
        return query
    def serialize_entry(self, data):
        return {
            'id':       data.genotype,
            'label':    data.genotype,
        }

class GetEffNote(handlers.standard.ListHandler):
    def create_query(self, data):
        query = VariationEffectNote.objects
        query = query.filter()
        return query
    def serialize_entry(self, data):
        return {
            'popcode':      data.popcode,
            'genotype':     data.genotype,
            'risk':         data.risk,
            'odd_ratio':    data.odd_ratio,
            'evidences':    data.evidences,
            'pmid':         data.pmid
        }
