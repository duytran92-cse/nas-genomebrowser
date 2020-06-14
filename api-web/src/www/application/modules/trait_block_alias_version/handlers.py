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
        query = TraitBlockAliasVersion.objects
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
        alias_version_helper = components.TraitBlockAliasVersionHelper()
        trait_block_version = TraitBlockAliasVersion.objects.get(pk=data['alias_id'])
        return {
            'id':               trait_block_version.id,
            'version':          trait_block_version.version,
            'version_status':   trait_block_version.version_status,
            'author':           trait_block_version.author,
            'trait_block':      trait_block_version.trait_block_id,
            'trait':            trait_block_version.trait_id,
            'created_at':       trait_block_version.created_at,
            'alias':            alias_version_helper.load_alias(trait_block_version.id),
        }

class Update(handlers.standard.UpdateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        return parser.get_data()
    def update(self, data):
        trait_block_version = TraitBlockAliasVersion.objects.get(pk=data['alias_id'])
        if 'author' in data:
            trait_block_version.author = data['author']
        if 'version_status' in data:
            trait_block_version.version_status = data['version_status']
        trait_block_version.is_stable = True
        trait_block_version.save()
        return trait_block_version


class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        trait = TraitBlockAliasVersion.objects.get(pk=data['alias_id'])
        trait.is_disabled = True
        trait.save()
        return 1

class Active(handlers.standard.DeleteHandler):
    def delete(self, data):
        block = TraitBlockAliasVersion.objects.get(pk=data['id'])
        # Update all block to inactive
        TraitBlockAliasVersion.objects.filter(trait_id=block.trait_id, trait_block_id=block.trait_block_id, version_status='active').update(version_status='inactive')
        # Update the request block to active
        block.version_status = 'active'
        block.save()
        return 1
