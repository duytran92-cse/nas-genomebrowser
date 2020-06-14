from notasquare.urad_api import *
from application.models import *
from application import constants
from . import components


class List(handlers.standard.ListHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('gene_id', 'integer'):
            self.add_error('gene_id', 'INVALID_DATA')
        return parser.get_data()
    def create_query(self, data):
        query = GeneBlock.objects
        query = query.filter(gene_id=data['gene_id'])
        query = query.filter(is_disabled=False)
        if 'kind' in data:
            if data['kind'] != '':
                query = query.filter(kind=data['kind'])
        if 'title' in data:
            query = query.filter(title__contains=data['text'])
        return query
    def serialize_entry(self, gene_block):
        # Get current version
        if gene_block.kind == 'general_text':
            query = GeneBlockVersion.objects.filter(gene_block_id=gene_block.id, version_status='active', is_disabled=False)
        elif gene_block.kind == 'general_alias':
            query = GeneBlockAliasVersion.objects.filter(gene_block_id=gene_block.id, version_status='active', is_disabled=False)
        elif gene_block.kind == 'general_publications':
            query = GeneBlockPublicationVersion.objects.filter(gene_block_id=gene_block.id, version_status='active', is_disabled=False)
        elif gene_block.kind == 'gene_infobox':
            query = GeneBlockInfoboxVersion.objects.filter(gene_block_id=gene_block.id, version_status='active', is_disabled=False)
        elif gene_block.kind == 'gene_effect':
            query = GeneBlockEffectVersion.objects.filter(gene_block_id=gene_block.id, version_status='active', is_disabled=False)

        active_version = query.filter(is_stable=True).order_by('-created_at')[:1]
        latest_version = query.order_by('-created_at')[:1]

        return {
            'id': gene_block.id,
            'title': gene_block.title,
            'text': gene_block.text,
            'kind': gene_block.kind,
            'position': gene_block.position,
            'sort_order': gene_block.sort_order,
            'gene': gene_block.gene_id,
            'active_version': active_version.first().version,
            'latest_version': latest_version.first().version
        }


class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        return components.GeneBlockHelper().load_gene_block(data['id'])

class Create(handlers.standard.CreateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('gene_id', 'integer'):
            self.add_error('gene_id', 'INVALID_DATA')
        if not parser.parse('kind', 'string'):
            self.add_error('kind', 'MUST_NOT_BE_EMPTY')
        if not parser.parse('position', 'string'):
            self.add_error('position', 'MUST_NOT_BE_EMPTY')
        if not parser.parse('title', 'string'):
            self.add_error('title', 'MUST_NOT_BE_EMPTY')
        if 'sort_order' in params:
            if not parser.parse('sort_order', 'integer'):
                self.add_error('sort_order', 'MUST_NOT_BE_EMPTY')
        return parser.get_data()
    def create(self, data):
        gene_block = GeneBlock()
        gene_block.gene_id = data['gene_id']
        gene_block.kind = data['kind']
        gene_block.position = data['position']
        gene_block.title = data['title']
        if 'sort_order' in data:
            gene_block.sort_order = data['sort_order']
        gene_block.save()

        return gene_block


class Update(handlers.standard.UpdateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('id', 'integer'):
            self.add_error('id', 'MUST_NOT_BE_EMPTY')
        if 'position' in params:
            if not parser.parse('position', 'string'):
                self.add_error('position', 'MUST_NOT_BE_EMPTY')
        if 'title' in params:
            if not parser.parse('title', 'string'):
                self.add_error('title', 'MUST_NOT_BE_EMPTY')
        if 'sort_order' in params:
            if not parser.parse('sort_order', 'integer'):
                self.add_error('sort_order', 'MUST_NOT_BE_EMPTY')

        gene_block = GeneBlock.objects.get(pk=params['id'])
        if gene_block.kind == 'general_publications':
            pass
        if gene_block.kind == 'gene_effect':
            pass

        return parser.get_data()
    def update(self, data):
        gene_block = GeneBlock.objects.get(pk=data['id'])
        gene = Gene.objects.get(pk=gene_block.gene_id)
        if 'position' in data:
            gene_block.position = data['position']
        if 'title' in data:
            gene_block.title = data['title']
        if 'sort_order' in data:
            gene_block.sort_order = data['sort_order']
        if 'text' in data:
            gene_block.text = data['text']
        gene_block.save()

        if gene_block.kind == 'general_text':
            gene_block_version = GeneBlockVersion()
            gene_block_version.gene_block_id = gene_block.id
            gene_block_version.gene_id = gene.id
            gene_block_version.title = data['title']
            gene_block_version.text = data['text']
            # When user create new version, make it active
            # Set status active
            gene_block_version.version_status = 'active'
            if 'verify' in data:
                gene_block_version.is_stable = True
            gene_block_version.author = 'anonymous' # Fix me
            # Set version
            version = GeneBlockVersion.objects.filter(gene_id=gene.id, gene_block_id=gene_block.id).aggregate(Max('version'))
            if version['version__max']:
                gene_block_version.version = int(version['version__max']) + 1
            gene_block_version.save()

        if gene_block.kind == 'general_publications':
            # if 'new_version' in data:
            gene_block_pub_version = GeneBlockPublicationVersion()
            gene_block_pub_version.gene_id = gene.id
            gene_block_pub_version.gene_block_id = gene_block.id
            # Set status active
            gene_block_pub_version.version_status = 'active'
            if 'verify' in data:
                gene_block_pub_version.is_stable = True
            gene_block_pub_version.author = 'anonymous' # Fix me
            # Set version
            version = GeneBlockPublicationVersion.objects.filter(gene_id=gene.id, gene_block_id=gene_block.id).aggregate(Max('version'))
            if version['version__max']:
                gene_block_pub_version.version = int(version['version__max']) + 1
            gene_block_pub_version.save()

            for publication in data['publications']:
                gene_block_publication = GeneBlockPublication()
                gene_block_publication.gene_block_id = gene_block.id
                gene_block_publication.gene_block_version_id = gene_block_pub_version.id
                gene_block_publication.pmid = publication['pmid']
                gene_block_publication.doi = publication['doi']
                gene_block_publication.pmc = publication['pmc']
                gene_block_publication.title = publication['title']
                gene_block_publication.authors = publication['authors']
                gene_block_publication.journal = publication['journal']
                gene_block_publication.save()

        if gene_block.kind == 'gene_effect':
            # if 'new_version' in data:
            gene_block_eff_version = GeneBlockEffectVersion()
            gene_block_eff_version.gene_block_id = gene_block.id
            gene_block_eff_version.gene_id = gene.id
            # Set status active
            gene_block_eff_version.version_status = 'active'
            if 'verify' in data:
                gene_block_eff_version.is_stable = True
            gene_block_eff_version.author = 'anonymous' # Fix me
            # Set version
            version = GeneBlockEffectVersion.objects.filter(gene_id=gene.id, gene_block_id=gene_block.id).aggregate(Max('version'))
            if version['version__max']:
                gene_block_eff_version.version = int(version['version__max']) + 1
            gene_block_eff_version.save()

            GeneBlockEffect.objects.filter(gene_block_id=gene_block.id).delete()
            for item in data['effects']:
                gene_block_effect = GeneBlockEffect()
                gene_block_effect.gene_block_id = gene_block.id
                gene_block_effect.gene_block_version_id = gene_block_eff_version.id
                gene_block_effect.type = item['type']
                gene_block_effect.effect = item['effect']
                gene_block_effect.publication = item['publication']
                gene_block_effect.evidences = item['evidences']
                gene_block_effect.save()
        if gene_block.kind == 'gene_infobox':
            gene_block_infobox_version = GeneBlockInfoboxVersion()
            gene_block_infobox_version.gene_id = gene.id
            gene_block_infobox_version.gene_block_id = gene_block.id
            # Set status active
            gene_block_infobox_version.version_status = 'active'
            if 'verify' in data:
                gene_block_infobox_version.is_stable = True
            gene_block_infobox_version.author = 'anonymous' # Fix me
            # Set version
            version = GeneBlockInfoboxVersion.objects.filter(gene_id=gene.id, gene_block_id=gene_block.id).aggregate(Max('version'))
            if version['version__max']:
                gene_block_infobox_version.version = int(version['version__max']) + 1
            gene_block_infobox_version.save()

            for item in data['infobox']:
                gene_block_infobox = GeneBlockInfobox()
                gene_block_infobox.gene_block_id = gene_block.id
                gene_block_infobox.gene_block_version_id = gene_block_infobox_version.id
                gene_block_infobox.description = item['description']
                gene_block_infobox.chromosome = item['chromosome']
                gene_block_infobox.start = item['start']
                gene_block_infobox.end = item['end']
                gene_block_infobox.number_of_exons = item['number_of_exons']
                gene_block_infobox.protein_products = item['protein_products']
                gene_block_infobox.save()
        if gene_block.kind == 'general_alias':
            gene_alias_version = GeneBlockAliasVersion()
            gene_alias_version.gene_id = gene.id
            gene_alias_version.gene_block_id = gene_block.id
            # Set status active
            gene_alias_version.version_status = 'active'
            if 'verify' in data:
                gene_alias_version.is_stable = True
            gene_alias_version.author = 'anonymous' # Fix me
            # Set version
            version = GeneBlockAliasVersion.objects.filter(gene_id=gene.id, gene_block_id=gene_block.id).aggregate(Max('version'))
            if version['version__max']:
                gene_alias_version.version = int(version['version__max']) + 1
            gene_alias_version.save()
            for item in data['alias']:
                gene_block_alias = GeneBlockAlias()
                gene_block_alias.gene_block_id = gene_block.id
                gene_block_alias.gene_block_version_id = gene_alias_version.id
                gene_block_alias.alias = item['alias']
                gene_block_alias.save()
        return gene_block


class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        gene_block = GeneBlock.objects.get(pk=data['id'])
        gene_block.is_disabled = True
        gene_block.save()
        return 1

class Helper(handlers.standard.GetHandler):
    def get_data(self, data):
        gene_block = GeneBlock.objects.get(pk=data['id'])
        gene = Gene.objects.get(pk=gene_block.gene_id)
        return {
            'title': gene.title
        }
