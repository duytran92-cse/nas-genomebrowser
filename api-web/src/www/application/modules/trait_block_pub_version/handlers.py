from notasquare.urad_api import *
from application.models import *
from application import constants
from . import components


class List(handlers.standard.ListHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('trait_block_id', 'integer'):
            self.add_error('trait_block_id', 'INVALID_DATA')
        return parser.get_data()
    def create_query(self, data):
        query = TraitBlockPublicationVersion.objects
        query = query.filter(trait_block_id=data['trait_block_id'])
        return query
    def serialize_entry(self, trait_block):
        return {
            'id':               trait_block.id,
            'version':          trait_block.version,
            'version_status':   trait_block.version_status,
            'author':           trait_block.author,
            'trait_block':      trait_block.trait_block_id,
            'trait':            trait_block.trait_id,
            'created_at':       trait_block.created_at,
            'verify':           trait_block.is_stable
        }

class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        pub_version_helper = components.TraitBlockPublicationVersionHelper()
        trait_block_version = TraitBlockPublicationVersion.objects.get(pk=data['pub_id'])
        return {
            'id':               trait_block_version.id,
            'version':          trait_block_version.version,
            'version_status':   trait_block_version.version_status,
            'author':           trait_block_version.author,
            'trait_block':      trait_block_version.trait_block_id,
            'trait':            trait_block_version.trait_id,
            'created_at':       trait_block_version.created_at,
            'publications':     pub_version_helper.load_publications(trait_block_version.id),
        }

class Update(handlers.standard.UpdateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if 'title' in params:
            if not parser.parse('title', 'string'):
                self.add_error('title', 'MUST_NOT_BE_EMPTY')
        if 'text' in params:
            if not parser.parse('text', 'string'):
                self.add_error('text', 'MUST_NOT_BE_EMPTY')
        if 'author' in params:
            if not parser.parse('author', 'string'):
                self.add_error('author', 'MUST_NOT_BE_EMPTY')
        return parser.get_data()
    def update(self, data):
        trait_block_version = TraitBlockPublicationVersion.objects.get(pk=data['pub_id'])
        if 'title' in data:
            trait_block_version.title = data['title']
        if 'text' in data:
            trait_block_version.text = data['text']
        if 'author' in data:
            trait_block_version.author = data['author']
        if 'version_status' in data:
            trait_block_version.version_status = data['version_status']
        trait_block_version.is_stable = True
        trait_block_version.save()
        return trait_block_version


class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        trait = TraitBlockPublicationVersion.objects.get(pk=data['pub_id'])
        trait.is_disabled = True
        trait.save()
        return 1
class Active(handlers.standard.DeleteHandler):
    def delete(self, data):
        block = TraitBlockPublicationVersion.objects.get(pk=data['id'])
        # Update all block to inactive
        TraitBlockPublicationVersion.objects.filter(gene_id=block.gene_id, gene_block_id=block.gene_block_id, version_status='active').update(version_status='inactive')
        # Update the request block to active
        block.version_status = 'active'
        block.save()
        return 1
