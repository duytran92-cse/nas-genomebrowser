from notasquare.urad_api import *
from application.models import *
from application import constants
from . import components


class List(handlers.standard.ListHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('treatment_id', 'integer'):
            self.add_error('treatment_id', 'INVALID_DATA')
        return parser.get_data()
    def create_query(self, data):
        query = TreatmentBlock.objects
        query = query.filter(treatment_id=data['treatment_id'])
        query = query.filter(is_disabled=False)
        if 'kind' in data:
            if data['kind'] != '':
                query = query.filter(kind=data['kind'])
        if 'title' in data:
            query = query.filter(title__contains=data['text'])
        return query
    def serialize_entry(self, treatment_block):
        # Get current version
        if treatment_block.kind == 'general_text':
            query = TreatmentBlockVersion.objects.filter(treatment_block_id=treatment_block.id, version_status='active', is_disabled=False)
        elif treatment_block.kind == 'general_alias':
            query = TreatmentBlockAliasVersion.objects.filter(treatment_block_id=treatment_block.id, version_status='active', is_disabled=False)
        elif treatment_block.kind == 'general_publications':
            query = TreatmentBlockPublicationVersion.objects.filter(treatment_block_id=treatment_block.id, version_status='active', is_disabled=False)
        
        active_version = query.filter(is_stable=True).order_by('-created_at')[:1]
        latest_version = query.order_by('-created_at')[:1]

        return {
            'id': treatment_block.id,
            'title': treatment_block.title,
            'text': treatment_block.text,
            'kind': treatment_block.kind,
            'position': treatment_block.position,
            'sort_order': treatment_block.sort_order,
            'treatment': treatment_block.treatment_id,
            'active_version': active_version.first().version,
            'latest_version': latest_version.first().version
        }

class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        return components.TreatmentBlockHelper().load_treatment_block(data['id'])

class Create(handlers.standard.CreateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('treatment_id', 'integer'):
            self.add_error('treatment_id', 'INVALID_DATA')
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
        treatment_block = TreatmentBlock()
        treatment_block.treatment_id = data['treatment_id']
        treatment_block.kind = data['kind']
        treatment_block.position = data['position']
        treatment_block.title = data['title']
        if 'sort_order' in data:
            treatment_block.sort_order = data['sort_order']
        treatment_block.save()

        return treatment_block


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

        treatment_block = TreatmentBlock.objects.get(pk=params['id'])
        if treatment_block.kind == 'general_publications':
            pass

        return parser.get_data()
    def update(self, data):
        treatment_block = TreatmentBlock.objects.get(pk=data['id'])
        treatment = Treatment.objects.get(pk=treatment_block.treatment_id)
        if 'position' in data:
            treatment_block.position = data['position']
        if 'title' in data:
            treatment_block.title = data['title']
        if 'sort_order' in data:
            treatment_block.sort_order = data['sort_order']
        if 'text' in data:
            treatment_block.text = data['text']
        treatment_block.save()

        if treatment_block.kind == 'general_text':
            treatment_block_version = TreatmentBlockVersion()
            treatment_block_version.treatment_block_id = treatment_block.id
            treatment_block_version.treatment_id = treatment.id
            treatment_block_version.title = data['title']
            treatment_block_version.text = data['text']
            # Set status active
            treatment_block_version.version_status = 'active'
            if 'verify' in data:
                treatment_block_version.is_stable = True
            treatment_block_version.author = 'anonymous' # Fix me
            # Set version
            version = TreatmentBlockVersion.objects.filter(treatment_id=treatment.id, treatment_block_id=treatment_block.id).aggregate(Max('version'))
            if version['version__max']:
                treatment_block_version.version = int(version['version__max']) + 1
            treatment_block_version.save()

        if treatment_block.kind == 'general_publications':
            # TreatmentBlockPublication.objects.filter(treatment_block_id=treatment_block.id).delete()
            # if 'new_version' in data:
            treatment_block_pub_version = TreatmentBlockPublicationVersion()
            treatment_block_pub_version.treatment_id = treatment.id
            treatment_block_pub_version.treatment_block_id = treatment_block.id
            # Set status active
            treatment_block_pub_version.version_status = 'active'
            if 'verify' in data:
                treatment_block_pub_version.is_stable = True
            treatment_block_pub_version.author = 'anonymous' # Fix me
            # Set version
            version = TreatmentBlockPublicationVersion.objects.filter(treatment_id=treatment.id, treatment_block_id=treatment_block.id).aggregate(Max('version'))
            if version['version__max']:
                treatment_block_pub_version.version = int(version['version__max']) + 1
            treatment_block_pub_version.save()

            for publication in data['publications']:
                treatment_block_publication = TreatmentBlockPublication()
                treatment_block_publication.treatment_block_id = treatment_block.id
                treatment_block_publication.treatment_block_version_id = treatment_block_pub_version.id
                treatment_block_publication.pmid = publication['pmid']
                treatment_block_publication.doi = publication['doi']
                treatment_block_publication.pmc = publication['pmc']
                treatment_block_publication.title = publication['title']
                treatment_block_publication.authors = publication['authors']
                treatment_block_publication.journal = publication['journal']
                treatment_block_publication.save()

        if treatment_block.kind == 'general_alias':
                treatment_alias_version = TreatmentBlockAliasVersion()
                treatment_alias_version.treatment_id = treatment.id
                treatment_alias_version.treatment_block_id = treatment_block.id
                # Set status active
                treatment_alias_version.version_status = 'active'
                if 'verify' in data:
                    treatment_alias_version.is_stable = True
                treatment_alias_version.author = 'anonymous' # Fix me
                # Set version
                version = TreatmentBlockAliasVersion.objects.filter(treatment_id=treatment.id, treatment_block_id=treatment_block.id).aggregate(Max('version'))
                if version['version__max']:
                    treatment_alias_version.version = int(version['version__max']) + 1
                treatment_alias_version.save()

                for item in data['alias']:
                    treatment_block_alias = TreatmentBlockAlias()
                    treatment_block_alias.treatment_block_id = treatment_block.id
                    treatment_block_alias.treatment_block_version_id = treatment_alias_version.id
                    treatment_block_alias.alias = item['alias']
                    treatment_block_alias.save()
        return treatment_block


class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        treatment_block = TreatmentBlock.objects.get(pk=data['id'])
        treatment_block.is_disabled = True
        treatment_block.save()
        return 1

class Helper(handlers.standard.GetHandler):
    def get_data(self, data):
        treatment_block = TreatmentBlock.objects.get(pk=data['id'])
        treatment = Treatment.objects.get(pk=treatment_block.treatment_id)
        return {
            'title': treatment.title
        }
