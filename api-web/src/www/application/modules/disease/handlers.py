from notasquare.urad_api import *
from application.models import *
from application import constants
from application.modules.disease import components
from application.modules.disease_block import components as block_components

class List(handlers.standard.ListHandler):
    def create_query(self, data):
        query = Disease.objects
        query = query.filter(is_disabled=False)
        if 'text' in data:
            query = query.filter(title__contains=data['text'])
        if 'letter' in data:
            if data['letter'] != 'all':
                query = query.filter(title__istartswith=data['letter'])
        return query
    def serialize_entry(self, data):
        helper = components.DataHelper()
        return {
            'id':       data.id,
            'title':    data.title,
            'associated_genes': helper.load_associated_genes(data.id),
            'associated_publications': helper.load_associated_publications(data.id),
        }

class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        result = {}
        helper = components.DataHelper()
        disease = Disease.objects.get(pk=data['id'])
        result['id']      = disease.id
        result['title']   = disease.title
        result['associated_genes']        = helper.load_associated_genes(data['id'])
        result['associated_publications'] = helper.load_associated_publications(data['id'])

        return result

class View(handlers.standard.GetHandler):
    def get_data(self, data):
        result = {}

        block_helper = block_components.DiseaseBlockHelper()

        disease = Disease.objects.get(title=data['id'])
        blocks = { 'main': [], 'left': [],'right': []}
        rows = DiseaseBlock.objects.filter(disease_id=disease.id, is_disabled = False).order_by('sort_order').all()
        for r in rows:
            block = block_helper.load_disease_block(r.id)
            blocks[r.position].append(block)
        result['id']      = disease.id
        result['title']   = disease.title
        result['blocks']  = blocks
        return result

class Create(handlers.standard.CreateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('title', 'string'):
            self.add_error('title', 'MUST_NOT_BE_EMPTY')
        return parser.get_data()
    def create(self, data):
        disease = Disease()
        disease.title = data['title']
        disease.save()
        # Save extra info
        DiseaseAssociatedGene.objects.filter(disease_id=disease.id).delete()
        for gene in data['associated_genes']:
            disease_ass_gene = DiseaseAssociatedGene()
            disease_ass_gene.gene_name = gene['gene_name']
            disease_ass_gene.disease_id = disease.id
            disease_ass_gene.save()

        DiseaseAssociatedPublication.objects.filter(disease_id=disease.id).delete()
        for publication in data['associated_publications']:
            disease_ass_publication = DiseaseAssociatedPublication()
            disease_ass_publication.disease_id = disease.id
            disease_ass_publication.pmid = publication['pmid']
            disease_ass_publication.doi = publication['doi']
            disease_ass_publication.pmc = publication['pmc']
            disease_ass_publication.title = publication['title']
            disease_ass_publication.authors = publication['authors']
            disease_ass_publication.journal = publication['journal']
            disease_ass_publication.save()
        return disease

class Update(handlers.standard.UpdateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if 'title' in params:
            if not parser.parse('title', 'string'):
                self.add_error('title', 'MUST_NOT_BE_EMPTY')
        return parser.get_data()
    def update(self, data):
        disease = Disease.objects.get(pk=data['id'])
        if 'title' in data:
            disease.title = data['title']
        disease.save()
        # Save extra info
        DiseaseAssociatedGene.objects.filter(disease_id=disease.id).delete()
        for gene in data['associated_genes']:
            disease_ass_gene = DiseaseAssociatedGene()
            disease_ass_gene.gene_name = gene['gene_name']
            disease_ass_gene.disease_id = disease.id
            disease_ass_gene.save()

        DiseaseAssociatedPublication.objects.filter(disease_id=disease.id).delete()
        for publication in data['associated_publications']:
            disease_ass_publication = DiseaseAssociatedPublication()
            disease_ass_publication.disease_id = disease.id
            disease_ass_publication.pmid = publication['pmid']
            disease_ass_publication.doi = publication['doi']
            disease_ass_publication.pmc = publication['pmc']
            disease_ass_publication.title = publication['title']
            disease_ass_publication.authors = publication['authors']
            disease_ass_publication.journal = publication['journal']
            disease_ass_publication.save()
        return disease


class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        disease = Disease.objects.get(pk=data['id'])
        disease.is_disabled = True
        disease.save()
        return 1

class Summary(handlers.standard.GetHandler):
    def get_data(self, data):
        result = []
        blocks = []
        comments = []
        active_blocks_version = []
        inactive_blocks_version = []

        disease = Disease.objects.get(pk=data['disease_id'])

        disease_genes = DiseaseAssociatedGene.objects.filter(disease_id=data['disease_id'])
        disease_gene = '111'
        if disease_genes:
            for item in disease_genes:
                disease_gene += ', ' + item.gene_name
        disease_gene = disease_gene.replace('111,','')

        disease_pubs = DiseaseAssociatedPublication.objects.filter(disease_id=data['disease_id'])
        disease_pub = []
        if disease_pubs:
            for item in disease_pubs:
                disease_pub.append('https://www.ncbi.nlm.nih.gov/pubmed/%s' % (item.pmid))

        disease_blocks = DiseaseBlock.objects.filter(disease_id=data['disease_id'],is_disabled=False)[:5]
        for item in disease_blocks:
            # Get active and latest version
            if item.kind == 'general_text':
                query = DiseaseBlockVersion.objects.filter(disease_block_id=item.id, version_status='active', is_disabled=False)
            elif item.kind == 'general_alias':
                query = DiseaseBlockAliasVersion.objects.filter(disease_block_id=item.id, version_status='active', is_disabled=False)
            elif item.kind == 'general_publications':
                query = DiseaseBlockPublicationVersion.objects.filter(disease_block_id=item.id, version_status='active', is_disabled=False)

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
                'page_id': item.disease_id,
                'active_version': ac_ver,
                'latest_version': l_ver
            })
        total_blocks = DiseaseBlock.objects.filter(disease_id=data['disease_id'],is_disabled=False).count()

        active_blocks_versions = DiseaseBlockVersion.objects.filter(disease_id=data['disease_id'],is_disabled=False, version_status='active')[:5]
        for item in active_blocks_versions:
            block = DiseaseBlock.objects.get(pk=item.disease_block_id)
            active_blocks_version.append({
                'id': item.id,
                'title': item.title,
                'text': item.text,
                'author': item.author,
                'version': item.version,
                'page_id': item.disease_id,
                'page_block_id': item.disease_block_id,
                'kind': block.kind,
                'timestamp': item.created_at
            })
        total_active_blocks_version = DiseaseBlockVersion.objects.filter(disease_id=data['disease_id'],is_disabled=False, version_status='active').count()

        inactive_blocks_versions = DiseaseBlockVersion.objects.filter(disease_id=data['disease_id'],is_disabled=False, version_status='inactive')[:10]
        for item in inactive_blocks_versions:
            block = DiseaseBlock.objects.get(pk=item.disease_block_id)
            inactive_blocks_version.append({
                'id': item.id,
                'title': item.title,
                'text': item.text,
                'author': item.author,
                'version': item.version,
                'page_id': item.disease_id,
                'page_block_id': item.disease_block_id,
                'kind': block.kind,
                'timestamp': item.created_at
            })
        total_inactive_blocks_version = DiseaseBlockVersion.objects.filter(disease_id=data['disease_id'],is_disabled=False, version_status='inactive').count()

        disease_comment = Comment.objects.filter(page='disease',entity=disease.title)[:5]

        for item in disease_comment:
            user = User.objects.get(pk=item.user_id)
            comments.append({
                'id': item.id,
                'timestamp': item.timestamp,
                'user': user.name,
                'comment': item.comment,
                'page_id': data['disease_id']
            })
        total_comments = Comment.objects.filter(page='disease',entity=disease.title).count()

        result.append({
            'disease_id': data['disease_id'],
            'title': disease.title,
            'disease_gene': disease_gene,
            'disease_pub': disease_pub,
            'blocks': blocks,
            'total_blocks': total_blocks,
            'total_active_blocks_version': total_active_blocks_version,
            'active_blocks_version': active_blocks_version,
            'total_inactive_blocks_version': total_inactive_blocks_version,
            'inactive_blocks_version': inactive_blocks_version,
            'total_comments': total_comments,
            'comments': comments
        })

        return (result)
