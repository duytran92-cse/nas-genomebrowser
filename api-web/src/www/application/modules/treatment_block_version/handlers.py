from notasquare.urad_api import *
from application.models import *
from application import constants

class List(handlers.standard.ListHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('treatment_block_id', 'integer'):
            self.add_error('treatment_block_id', 'INVALID_DATA')
        return parser.get_data()
    def create_query(self, data):
        query = TreatmentBlockVersion.objects
        query = query.filter(treatment_block_id=data['treatment_block_id'])
        return query
    def serialize_entry(self, treatment_block):
        return {
            'id':               treatment_block.id,
            'version':          treatment_block.version,
            'version_status':   treatment_block.version_status,
            'text':             treatment_block.text,
            'title':            treatment_block.title,
            'author':           treatment_block.author,
            'treatment_block':  treatment_block.treatment_block_id,
            'treatment':        treatment_block.treatment_id,
            'created_at':       treatment_block.created_at,
            'verify':           treatment_block.is_stable
        }

class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        treatment_block_version = TreatmentBlockVersion.objects.get(pk=data['text_id'])
        return {
            'id':               treatment_block_version.id,
            'version':          treatment_block_version.version,
            'version_status':   treatment_block_version.version_status,
            'text':             treatment_block_version.text,
            'title':            treatment_block_version.title,
            'author':           treatment_block_version.author,
            'treatment_block':  treatment_block_version.treatment_block_id,
            'treatment':        treatment_block_version.treatment_id,
            'created_at':       treatment_block_version.created_at
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
        treatment_block_version = TreatmentBlockVersion.objects.get(pk=data['text_id'])
        if 'title' in data:
            treatment_block_version.title = data['title']
        if 'text' in data:
            treatment_block_version.text = data['text']
        if 'author' in data:
            treatment_block_version.author = data['author']
        if 'version_status' in data:
            treatment_block_version.version_status = data['version_status']
        treatment_block_version.is_stable = True
        treatment_block_version.save()
        return treatment_block_version

class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        block = TreatmentBlockVersion.objects.get(pk=data['id'])
        block.is_disabled = True
        block.save()
        return 1

class Active(handlers.standard.DeleteHandler):
    def delete(self, data):
        block = TreatmentBlockVersion.objects.get(pk=data['id'])
        # Update all block to inactive
        TreatmentBlockVersion.objects.filter(treatment_id=block.treatment_id, treatment_block_id=block.treatment_block_id, version_status='active').update(version_status='inactive')
        # Update the request block to active
        block.version_status = 'active'
        block.save()
        return 1
