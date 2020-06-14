from notasquare.urad_api import *
from application.models import *
from application import constants

class List(handlers.standard.ListHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('disease_block_id', 'integer'):
            self.add_error('disease_block_id', 'INVALID_DATA')
        return parser.get_data()
    def create_query(self, data):
        query = DiseaseBlockVersion.objects
        query = query.filter(disease_block_id=data['disease_block_id'])
        return query
    def serialize_entry(self, disease_block):
        return {
            'id':               disease_block.id,
            'version':          disease_block.version,
            'version_status':   disease_block.version_status,
            'text':             disease_block.text,
            'title':            disease_block.title,
            'author':           disease_block.author,
            'disease_block':    disease_block.disease_block_id,
            'disease':          disease_block.disease_id,
            'created_at':       disease_block.created_at,
            'verify':           disease_block.is_stable
        }
class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        disease_block_version = DiseaseBlockVersion.objects.get(pk=data['text_id'])
        return {
            'id':               disease_block_version.id,
            'version':          disease_block_version.version,
            'version_status':   disease_block_version.version_status,
            'text':             disease_block_version.text,
            'title':            disease_block_version.title,
            'author':           disease_block_version.author,
            'disease_block':    disease_block_version.disease_block_id,
            'disease':          disease_block_version.disease_id,
            'created_at':       disease_block_version.created_at
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
        disease_block_version = DiseaseBlockVersion.objects.get(pk=data['text_id'])
        if 'title' in data:
            disease_block_version.title = data['title']
        if 'text' in data:
            disease_block_version.text = data['text']
        if 'author' in data:
            disease_block_version.author = data['author']
        if 'version_status' in data:
            disease_block_version.version_status = data['version_status']
        disease_block_version.is_stable = True
        disease_block_version.save()
        return disease_block_version

class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        block = DiseaseBlockVersion.objects.get(pk=data['id'])
        block.is_disabled = True
        block.save()
        return 1

class Active(handlers.standard.DeleteHandler):
    def delete(self, data):
        block = DiseaseBlockVersion.objects.get(pk=data['id'])
        # Update all block to inactive
        DiseaseBlockVersion.objects.filter(disease_id=block.disease_id, disease_block_id=block.disease_block_id, version_status='active').update(version_status='inactive')
        # Update the request block to active
        block.version_status = 'active'
        block.save()
        return 1
