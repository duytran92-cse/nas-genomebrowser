from notasquare.urad_api import *
from application.models import *
from application import constants
from . import components


class List(handlers.standard.ListHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('trait_id', 'integer'):
            self.add_error('trait_id', 'INVALID_DATA')
        return parser.get_data()
    def create_query(self, data):
        query = TraitBlock.objects
        query = query.filter(trait_id=data['trait_id'])
        query = query.filter(is_disabled=False)
        if 'kind' in data:
            if data['kind'] != '':
                query = query.filter(kind=data['kind'])
        if 'title' in data:
            query = query.filter(title__contains=data['text'])
        return query
    def serialize_entry(self, trait_block):
        # Get current version
        if trait_block.kind == 'general_text':
            query = TraitBlockVersion.objects.filter(trait_block_id=trait_block.id, version_status='active', is_disabled=False)
        elif trait_block.kind == 'general_alias':
            query = TraitBlockAliasVersion.objects.filter(trait_block_id=trait_block.id, version_status='active', is_disabled=False)
        elif trait_block.kind == 'general_publications':
            query = TraitBlockPublicationVersion.objects.filter(trait_block_id=trait_block.id, version_status='active', is_disabled=False)
        
        active_version = query.filter(is_stable=True).order_by('-created_at')[:1]
        latest_version = query.order_by('-created_at')[:1]

        return {
            'id': trait_block.id,
            'title': trait_block.title,
            'text': trait_block.text,
            'kind': trait_block.kind,
            'position': trait_block.position,
            'sort_order': trait_block.sort_order,
            'trait': trait_block.trait_id,
            'active_version': active_version.first().version,
            'latest_version': latest_version.first().version
        }


class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        return components.TraitBlockHelper().load_trait_block(data['id'])

class Create(handlers.standard.CreateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('trait_id', 'integer'):
            self.add_error('trait_id', 'INVALID_DATA')
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
        trait_block = TraitBlock()
        trait_block.trait_id = data['trait_id']
        trait_block.kind = data['kind']
        trait_block.position = data['position']
        trait_block.title = data['title']
        if 'sort_order' in data:
            trait_block.sort_order = data['sort_order']
        trait_block.save()

        return trait_block


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

        trait_block = TraitBlock.objects.get(pk=params['id'])
        if trait_block.kind == 'general_publications':
            pass

        return parser.get_data()
    def update(self, data):
        trait_block = TraitBlock.objects.get(pk=data['id'])
        trait = Trait.objects.get(pk=trait_block.trait_id)
        if 'position' in data:
            trait_block.position = data['position']
        if 'title' in data:
            trait_block.title = data['title']
        if 'sort_order' in data:
            trait_block.sort_order = data['sort_order']
        if 'text' in data:
            trait_block.text = data['text']
        trait_block.save()

        if trait_block.kind == 'general_text':
            trait_block_version = TraitBlockVersion()
            trait_block_version.trait_block_id = trait_block.id
            trait_block_version.trait_id = trait.id
            trait_block_version.title = data['title']
            trait_block_version.text = data['text']
            # Set status active
            trait_block_version.version_status = 'active'
            if 'verify' in data:
                trait_block_version.is_stable = True
            trait_block_version.author = 'anonymous' # Fix me
            # Set version
            version = TraitBlockVersion.objects.filter(trait_id=trait.id, trait_block_id=trait_block.id).aggregate(Max('version'))
            if version['version__max']:
                trait_block_version.version = int(version['version__max']) + 1
            trait_block_version.save()

        if trait_block.kind == 'general_publications':
            # if 'new_version' in data:
            trait_block_pub_version = TraitBlockPublicationVersion()
            trait_block_pub_version.trait_id = trait.id
            trait_block_pub_version.trait_block_id = trait_block.id
            trait_block_pub_version.version_status = 'active' # Fix me
            if 'verify' in data:
                trait_block_pub_version.is_stable = True
            trait_block_pub_version.author = 'anonymous' # Fix me
            # Set version
            version = TraitBlockPublicationVersion.objects.filter(trait_id=trait.id, trait_block_id=trait_block.id).aggregate(Max('version'))
            if version['version__max']:
                trait_block_pub_version.version = int(version['version__max']) + 1
            trait_block_pub_version.save()

            for publication in data['publications']:
                trait_block_publication = TraitBlockPublication()
                trait_block_publication.trait_block_id = trait_block.id
                trait_block_publication.trait_block_version_id = trait_block_pub_version.id
                trait_block_publication.pmid = publication['pmid']
                trait_block_publication.doi = publication['doi']
                trait_block_publication.pmc = publication['pmc']
                trait_block_publication.title = publication['title']
                trait_block_publication.authors = publication['authors']
                trait_block_publication.journal = publication['journal']
                trait_block_publication.save()

        if trait_block.kind == 'general_alias':
                trait_alias_version = TraitBlockAliasVersion()
                trait_alias_version.trait_id = trait.id
                trait_alias_version.trait_block_id = trait_block.id
                trait_alias_version.version_status = 'active' # Fix me
                if 'verify' in data:
                    trait_alias_version.is_stable = True
                trait_alias_version.author = 'anonymous' # Fix me
                # Set version
                version = TraitBlockAliasVersion.objects.filter(trait_id=trait.id, trait_block_id=trait_block.id).aggregate(Max('version'))
                if version['version__max']:
                    trait_alias_version.version = int(version['version__max']) + 1
                trait_alias_version.save()

                for item in data['alias']:
                    trait_block_alias = TraitBlockAlias()
                    trait_block_alias.trait_block_id = trait_block.id
                    trait_block_alias.trait_block_version_id = trait_alias_version.id
                    trait_block_alias.alias = item['alias']
                    trait_block_alias.save()
        return trait_block


class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        trait_block = TraitBlock.objects.get(pk=data['id'])
        trait_block.is_disabled = True
        trait_block.save()
        return 1
class Helper(handlers.standard.GetHandler):
    def get_data(self, data):
        trait_block = TraitBlock.objects.get(pk=data['id'])
        trait = Trait.objects.get(pk=trait_block.trait_id)
        return {
            'title': trait.title
        }
