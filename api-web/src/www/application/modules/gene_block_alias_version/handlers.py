from notasquare.urad_api import *
from application.models import *
from application import constants
from . import components

class List(handlers.standard.ListHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('gene_block_id', 'integer'):
            self.add_error('gene_block_id', 'INVALID_DATA')
        return parser.get_data()
    def create_query(self, data):
        query = GeneBlockAliasVersion.objects
        query = query.filter(gene_block_id=data['gene_block_id'])
        return query
    def serialize_entry(self, gene_block):
        return {
            'id':               gene_block.id,
            'version':          gene_block.version,
            'version_status':   gene_block.version_status,
            'author':           gene_block.author,
            'gene_block':       gene_block.gene_block_id,
            'gene':             gene_block.gene_id,
            'created_at':       gene_block.created_at,
            'verify':           gene_block.is_stable
        }

class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        alias_version_helper = components.GeneBlockAliasVersionHelper()
        gene_block_version = GeneBlockAliasVersion.objects.get(pk=data['alias_id'])
        return {
            'id':               gene_block_version.id,
            'version':          gene_block_version.version,
            'version_status':   gene_block_version.version_status,
            'author':           gene_block_version.author,
            'gene_block':       gene_block_version.gene_block_id,
            'gene':             gene_block_version.gene_id,
            'alias':            alias_version_helper.load_alias(gene_block_version.id),
            'created_at':       gene_block_version.created_at
        }

class Update(handlers.standard.UpdateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        return parser.get_data()
    def update(self, data):
        gene_block_version = GeneBlockAliasVersion.objects.get(pk=data['alias_id'])
        if 'author' in data:
            gene_block_version.author = data['author']
        if 'version_status' in data:
            gene_block_version.version_status = data['version_status']
        gene_block_version.is_stable = True
        gene_block_version.save()
        return gene_block_version


class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        gene = GeneBlockAliasVersion.objects.get(pk=data['alias_id'])
        gene.is_disabled = True
        gene.save()
        return 1

class Active(handlers.standard.DeleteHandler):
    def delete(self, data):
        block = GeneBlockAliasVersion.objects.get(pk=data['id'])
        # Update all block to inactive
        GeneBlockAliasVersion.objects.filter(gene_id=block.gene_id, gene_block_id=block.gene_block_id, version_status='active').update(version_status='inactive')
        # Update the request block to active
        block.version_status = 'active'
        block.save()
        return 1
