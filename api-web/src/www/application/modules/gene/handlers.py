from notasquare.urad_api import *
from application.models import *
from application import constants
from application.modules.gene import components
from application.modules.gene_block import components as block_components

class List(handlers.standard.ListHandler):
    def create_query(self, data):
        query = Gene.objects
        query = query.filter(is_disabled=False)
        if 'text' in data:
            query = query.filter(title__contains=data['text'])
        if 'letter' in data:
            if data['letter'] != 'all':
                query = query.filter(title__istartswith=data['letter'])
        if 'isDisease' in data:
            query = query.filter(num_associated_disease__gt = 0)
        if 'isPub' in data:
            query = query.filter(num_associated_publication__gt = 0)
        return query
    def serialize_entry(self, data):
        helper = components.DataHelper()
        return {
            'id':       data.id,
            'title':    data.title,
            'associated_diseases': helper.load_associated_diseases(data.id),
            'associated_diseases_group_name':          helper.load_associated_diseases_group_name(data.id),
            'associated_publications': helper.load_associated_publications(data.id)
        }

class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        result = {}
        helper = components.DataHelper()
        gene = Gene.objects.get(pk=data['id'])
        result['id']      = gene.id
        result['title']   = gene.title
        result['associated_diseases']     = helper.load_associated_diseases(data['id'])
        result['associated_publications'] = helper.load_associated_publications(data['id'])


        return result

class View(handlers.standard.GetHandler):
    def get_data(self, data):
        result = {}
        block_helper = block_components.GeneBlockHelper()

        gene = Gene.objects.get(title=data['id'])
        blocks = { 'main': [], 'left': [],'right': []}
        rows = GeneBlock.objects.filter(gene_id=gene.id, is_disabled = False).order_by('sort_order').all()
        for r in rows:
            block = block_helper.load_gene_block(r.id)
            blocks[r.position].append(block)
        result['id']      = gene.id
        result['title']   = gene.title
        result['blocks']  = blocks
        return result

class Create(handlers.standard.CreateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('title', 'string'):
            self.add_error('title', 'MUST_NOT_BE_EMPTY')
        return parser.get_data()
    def create(self, data):
        gene = Gene()
        gene.title = data['title']
        gene.save()
        # Save extra info
        for disease in data['associated_diseases']:
            gene_ass_disease = GeneAssociatedDisease()
            gene_ass_disease.disease_name = disease['disease_name']
            gene_ass_disease.gene_id = gene.id
            gene_ass_disease.save()

        for publication in data['associated_publications']:
            gene_ass_publication = GeneAssociatedPublication()
            gene_ass_publication.gene_id = gene.id
            gene_ass_publication.pmid = publication['pmid']
            gene_ass_publication.doi = publication['doi']
            gene_ass_publication.pmc = publication['pmc']
            gene_ass_publication.title = publication['title']
            gene_ass_publication.authors = publication['authors']
            gene_ass_publication.journal = publication['journal']
            gene_ass_publication.save()

        return gene

class Update(handlers.standard.UpdateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if 'title' in params:
            if not parser.parse('title', 'string'):
                self.add_error('title', 'MUST_NOT_BE_EMPTY')
        return parser.get_data()
    def update(self, data):
        gene = Gene.objects.get(pk=data['id'])
        if 'title' in data:
            gene.title = data['title']
        gene.save()
        # Save extra info
        GeneAssociatedDisease.objects.filter(gene_id=gene.id).delete()
        for disease in data['associated_diseases']:
            gene_ass_disease = GeneAssociatedDisease()
            gene_ass_disease.disease_name = disease['disease_name']
            gene_ass_disease.gene_id = gene.id
            gene_ass_disease.save()


        GeneAssociatedPublication.objects.filter(gene_id=gene.id).delete()
        for publication in data['associated_publications']:
            gene_ass_publication = GeneAssociatedPublication()
            gene_ass_publication.gene_id = gene.id
            gene_ass_publication.pmid = publication['pmid']
            gene_ass_publication.doi = publication['doi']
            gene_ass_publication.pmc = publication['pmc']
            gene_ass_publication.title = publication['title']
            gene_ass_publication.authors = publication['authors']
            gene_ass_publication.journal = publication['journal']
            gene_ass_publication.save()

        return gene


class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        gene = Gene.objects.get(pk=data['id'])
        gene.is_disabled = True
        gene.save()
        return 1

class Summary(handlers.standard.GetHandler):
    def get_data(self, data):
        result = []
        blocks = []
        comments = []
        active_blocks_version = []
        inactive_blocks_version = []

        gene = Gene.objects.get(pk=data['gene_id'])

        gene_diseases = GeneAssociatedDisease.objects.filter(gene_id=data['gene_id'])
        gene_disease = '111'
        if gene_diseases:
            for item in gene_diseases:
                gene_disease += ', ' + item.disease_name
        gene_disease = gene_disease.replace('111,','')

        gene_blocks = GeneBlock.objects.filter(gene_id=data['gene_id'],is_disabled=False)[:5]
        for item in gene_blocks:

            # Get active and latest version
            if item.kind == 'general_text':
                query = GeneBlockVersion.objects.filter(gene_block_id=item.id, version_status='active', is_disabled=False)
            elif item.kind == 'general_alias':
                query = GeneBlockAliasVersion.objects.filter(gene_block_id=item.id, version_status='active', is_disabled=False)
            elif item.kind == 'general_publications':
                query = GeneBlockPublicationVersion.objects.filter(gene_block_id=item.id, version_status='active', is_disabled=False)
            elif item.kind == 'gene_infobox':
                query = GeneBlockInfoboxVersion.objects.filter(gene_block_id=item.id, version_status='active', is_disabled=False)
            elif item.kind == 'gene_effect':
                query = GeneBlockEffectVersion.objects.filter(gene_block_id=item.id, version_status='active', is_disabled=False)

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
                'page_id': item.gene_id,
                'active_version': ac_ver,
                'latest_version': l_ver
            })
        total_blocks = GeneBlock.objects.filter(gene_id=data['gene_id'],is_disabled=False).count()

        active_blocks_versions = GeneBlockVersion.objects.filter(gene_id=data['gene_id'],is_disabled=False, version_status='active')[:5]
        for item in active_blocks_versions:
            block = GeneBlock.objects.get(pk=item.gene_block_id)
            active_blocks_version.append({
                'id': item.id,
                'title': item.title,
                'text': item.text,
                'author': item.author,
                'version': item.version,
                'page_id': item.gene_id,
                'page_block_id': item.gene_block_id,
                'kind': block.kind,
                'timestamp': item.created_at
            })
        total_active_blocks_version = GeneBlockVersion.objects.filter(gene_id=data['gene_id'],is_disabled=False, version_status='active').count()

        inactive_blocks_versions = GeneBlockVersion.objects.filter(gene_id=data['gene_id'],is_disabled=False, version_status='inactive')[:10]
        for item in inactive_blocks_versions:
            block = GeneBlock.objects.get(pk=item.gene_block_id)
            inactive_blocks_version.append({
                'id': item.id,
                'title': item.title,
                'text': item.text,
                'author': item.author,
                'version': item.version,
                'page_id': item.gene_id,
                'page_block_id': item.gene_block_id,
                'kind': block.kind,
                'timestamp': item.created_at
            })
        total_inactive_blocks_version = GeneBlockVersion.objects.filter(gene_id=data['gene_id'],is_disabled=False, version_status='inactive').count()

        gene_comment = Comment.objects.filter(page='gene',entity=gene.title)[:5]

        for item in gene_comment:
            user = User.objects.get(pk=item.user_id)
            comments.append({
                'id': item.id,
                'timestamp': item.timestamp,
                'user': user.name,
                'comment': item.comment,
                'page_id': data['gene_id']
            })
        total_comments = Comment.objects.filter(page='gene',entity=gene.title).count()

        result.append({
            'gene_id': data['gene_id'],
            'title': gene.title,
            'gene_disease': gene_disease,
            'blocks': blocks,
            'total_blocks': total_blocks,
            'total_active_blocks_version': total_active_blocks_version,
            'active_blocks_version': active_blocks_version,
            'total_inactive_blocks_version': total_inactive_blocks_version,
            'inactive_blocks_version': inactive_blocks_version,
            'total_comments': total_comments,
            'comments': comments
        })
        print result
        return (result)
