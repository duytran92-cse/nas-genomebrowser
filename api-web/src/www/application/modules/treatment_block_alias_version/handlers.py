from notasquare.urad_api import *
from application.models import *
from application import constants
from . import components


class List(handlers.standard.ListHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('treatment_block_id', 'integer'):
            self.add_error('treatment_block_id', 'INVALID_DATA')
        return parser.get_data()
    def create_query(self, data):
        query = TreatmentBlockAliasVersion.objects
        query = query.filter(treatment_block_id=data['treatment_block_id'])
        return query
    def serialize_entry(self, treatment_block):
        return {
            'id':               treatment_block.id,
            'version':          treatment_block.version,
            'version_status':   treatment_block.version_status,
            'author':           treatment_block.author,
            'treatment_block':  treatment_block.treatment_block_id,
            'treatment':        treatment_block.treatment_id,
            'created_at':       treatment_block.created_at,
            'verify':           treatment_block.is_stable
        }

class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        alias_version_helper = components.TreatmentBlockAliasVersionHelper()
        treatment_block_version = TreatmentBlockAliasVersion.objects.get(pk=data['alias_id'])
        return {
            'id':               treatment_block_version.id,
            'version':          treatment_block_version.version,
            'version_status':   treatment_block_version.version_status,
            'author':           treatment_block_version.author,
            'treatment_block':  treatment_block_version.treatment_block_id,
            'treatment':        treatment_block_version.treatment_id,
            'created_at':       treatment_block_version.created_at,
            'alias':            alias_version_helper.load_alias(treatment_block_version.id),
        }

class Update(handlers.standard.UpdateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        return parser.get_data()
    def update(self, data):
        treatment_block_version = TreatmentBlockAliasVersion.objects.get(pk=data['alias_id'])
        if 'author' in data:
            treatment_block_version.author = data['author']
        if 'version_status' in data:
            treatment_block_version.version_status = data['version_status']
        treatment_block_version.is_stable = True
        treatment_block_version.save()
        return treatment_block_version


class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        treatment = TreatmentBlockAliasVersion.objects.get(pk=data['alias_id'])
        treatment.is_disabled = True
        treatment.save()
        return 1

class Active(handlers.standard.DeleteHandler):
    def delete(self, data):
        block = TreatmentBlockAliasVersion.objects.get(pk=data['id'])
        # Update all block to inactive
        TreatmentBlockAliasVersion.objects.filter(treatment_id=block.treatment_id, treatment_block_id=block.treatment_block_id, version_status='active').update(version_status='inactive')
        # Update the request block to active
        block.version_status = 'active'
        block.save()
        return 1
