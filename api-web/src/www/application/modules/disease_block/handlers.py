from notasquare.urad_api import *
from application.models import *
from application import constants
from . import components


class List(handlers.standard.ListHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('disease_id', 'integer'):
            self.add_error('disease_id', 'INVALID_DATA')
        return parser.get_data()
    def create_query(self, data):
        query = DiseaseBlock.objects
        query = query.filter(disease_id=data['disease_id'])
        query = query.filter(is_disabled=False)
        if 'kind' in data:
            if data['kind'] != '':
                query = query.filter(kind=data['kind'])
        if 'title' in data:
            query = query.filter(title__contains=data['text'])
        return query
    def serialize_entry(self, disease_block):
        # Get current version
        if disease_block.kind == 'general_text':
            query = DiseaseBlockVersion.objects.filter(disease_block_id=disease_block.id, version_status='active', is_disabled=False)
        elif disease_block.kind == 'general_alias':
            query = DiseaseBlockAliasVersion.objects.filter(disease_block_id=disease_block.id, version_status='active', is_disabled=False)
        elif disease_block.kind == 'general_publications':
            query = DiseaseBlockPublicationVersion.objects.filter(disease_block_id=disease_block.id, version_status='active', is_disabled=False)
        
        active_version = query.filter(is_stable=True).order_by('-created_at')[:1]
        latest_version = query.order_by('-created_at')[:1]
        
        return {
            'id': disease_block.id,
            'title': disease_block.title,
            'text': disease_block.text,
            'kind': disease_block.kind,
            'position': disease_block.position,
            'sort_order': disease_block.sort_order,
            'disease': disease_block.disease_id,
            'active_version': active_version.first().version,
            'latest_version': latest_version.first().version
        }


class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        return components.DiseaseBlockHelper().load_disease_block(data['id'])

class Create(handlers.standard.CreateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('disease_id', 'integer'):
            self.add_error('disease_id', 'INVALID_DATA')
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
        disease_block = DiseaseBlock()
        disease_block.disease_id = data['disease_id']
        disease_block.kind = data['kind']
        disease_block.position = data['position']
        disease_block.title = data['title']
        if 'sort_order' in data:
            disease_block.sort_order = data['sort_order']
        disease_block.save()

        return disease_block


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

        disease_block = DiseaseBlock.objects.get(pk=params['id'])
        if disease_block.kind == 'general_publications':
            pass

        return parser.get_data()
    def update(self, data):
        disease_block = DiseaseBlock.objects.get(pk=data['id'])
        disease = Disease.objects.get(pk=disease_block.disease_id)
        if 'position' in data:
            disease_block.position = data['position']
        if 'title' in data:
            disease_block.title = data['title']
        if 'sort_order' in data:
            disease_block.sort_order = data['sort_order']
        if 'text' in data:
            disease_block.text = data['text']
        disease_block.save()

        if disease_block.kind == 'general_text':
            disease_block_version = DiseaseBlockVersion()
            disease_block_version.disease_block_id = disease_block.id
            disease_block_version.disease_id = disease.id
            disease_block_version.title = data['title']
            disease_block_version.text = data['text']
            # When user create new version, make it active
            # Set status active
            disease_block_version.version_status = 'active'
            if 'verify' in data:
                disease_block_version.is_stable = True
            disease_block_version.author = 'anonymous' # Fix me
            # Set version
            version = DiseaseBlockVersion.objects.filter(disease_id=disease.id, disease_block_id=disease_block.id).aggregate(Max('version'))
            if version['version__max']:
                disease_block_version.version = int(version['version__max']) + 1
            disease_block_version.save()

        if disease_block.kind == 'general_publications':
            # DiseaseBlockPublication.objects.filter(disease_block_id=disease_block.id).delete()
            # if 'new_version' in data:
            disease_block_pub_version = DiseaseBlockPublicationVersion()
            disease_block_pub_version.disease_id = disease.id
            disease_block_pub_version.disease_block_id = disease_block.id
            # Set status active
            disease_block_pub_version.version_status = 'active'
            if 'verify' in data:
                disease_block_pub_version.is_stable = True
            disease_block_pub_version.author = 'anonymous' # Fix me
            # Set version
            version = DiseaseBlockPublicationVersion.objects.filter(disease_id=disease.id, disease_block_id=disease_block.id).aggregate(Max('version'))
            if version['version__max']:
                disease_block_pub_version.version = int(version['version__max']) + 1
            disease_block_pub_version.save()

            for publication in data['publications']:
                disease_block_publication = DiseaseBlockPublication()
                disease_block_publication.disease_block_id = disease_block.id
                disease_block_publication.disease_block_version_id = disease_block_pub_version.id
                disease_block_publication.pmid = publication['pmid']
                disease_block_publication.doi = publication['doi']
                disease_block_publication.pmc = publication['pmc']
                disease_block_publication.title = publication['title']
                disease_block_publication.authors = publication['authors']
                disease_block_publication.journal = publication['journal']
                disease_block_publication.save()
        if disease_block.kind == 'general_alias':
            disease_alias_version = DiseaseBlockAliasVersion()
            disease_alias_version.disease_id = disease.id
            disease_alias_version.disease_block_id = disease_block.id
            # Set status active
            disease_alias_version.version_status = 'active'
            if 'verify' in data:
                disease_alias_version.is_stable = True
            disease_alias_version.author = 'anonymous' # Fix me
            # Set version
            version = DiseaseBlockAliasVersion.objects.filter(disease_id=disease.id, disease_block_id=disease_block.id).aggregate(Max('version'))
            if version['version__max']:
                disease_alias_version.version = int(version['version__max']) + 1
            disease_alias_version.save()
            for item in data['alias']:
                disease_block_alias = DiseaseBlockAlias()
                disease_block_alias.disease_block_id = disease_block.id
                disease_block_alias.disease_block_version_id = disease_alias_version.id
                disease_block_alias.alias = item['alias']
                disease_block_alias.save()

        return disease_block


class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        disease_block = DiseaseBlock.objects.get(pk=data['id'])
        disease_block.is_disabled = True
        disease_block.save()
        return 1

class Helper(handlers.standard.GetHandler):
    def get_data(self, data):
        disease_block = DiseaseBlock.objects.get(pk=data['id'])
        disease = Disease.objects.get(pk=disease_block.disease_id)
        return {
            'title': disease.title
        }
