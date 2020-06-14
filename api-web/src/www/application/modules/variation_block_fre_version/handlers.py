from notasquare.urad_api import *
from application.models import *
from application import constants
from . import components


class List(handlers.standard.ListHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('variation_block_id', 'integer'):
            self.add_error('variation_block_id', 'INVALID_DATA')
        return parser.get_data()
    def create_query(self, data):
        query = VariationBlockFrequencyVersion.objects
        query = query.filter(variation_block_id=data['variation_block_id'])
        return query
    def serialize_entry(self, variation_block):
        return {
            'id':               variation_block.id,
            'version':          variation_block.version,
            'version_status':   variation_block.version_status,
            'author':           variation_block.author,
            'variation_block':  variation_block.variation_block_id,
            'variation':        variation_block.variation_id,
            'created_at':       variation_block.created_at,
            'verify':           variation_block.is_stable
        }

class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        fre_version_helper = components.VariationBlockFrequencyVersionHelper()
        variation_block_version = VariationBlockFrequencyVersion.objects.get(pk=data['fre_id'])
        return {
            'id':               variation_block_version.id,
            'version':          variation_block_version.version,
            'version_status':   variation_block_version.version_status,
            'author':           variation_block_version.author,
            'variation_block':  variation_block_version.variation_block_id,
            'variation':        variation_block_version.variation_id,
            'created_at':       variation_block_version.created_at,
            'frequencies':      fre_version_helper.load_frequencies(variation_block_version.id),
        }

class Update(handlers.standard.UpdateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if 'author' in params:
            if not parser.parse('author', 'string'):
                self.add_error('author', 'MUST_NOT_BE_EMPTY')
        return parser.get_data()
    def update(self, data):
        variation_block_version = VariationBlockFrequencyVersion.objects.get(pk=data['fre_id'])
        if 'author' in data:
            variation_block_version.author = data['author']
        if 'version_status' in data:
            variation_block_version.version_status = data['version_status']
        variation_block_version.is_stable = True
        variation_block_version.save()
        return variation_block_version


class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        variation = VariationBlockFrequencyVersion.objects.get(pk=data['fre_id'])
        variation.is_disabled = True
        variation.save()
        return 1

class Active(handlers.standard.DeleteHandler):
    def delete(self, data):
        block = VariationBlockFrequencyVersion.objects.get(pk=data['id'])
        # Update all block to inactive
        VariationBlockFrequencyVersion.objects.filter(variation_id=block.variation_id, variation_block_id=block.variation_block_id, version_status='active').update(version_status='inactive')
        # Update the request block to active
        block.version_status = 'active'
        block.save()
        return 1
