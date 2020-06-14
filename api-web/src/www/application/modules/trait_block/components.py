
from application.models import *

class TraitBlockHelper(object):
    def load_trait_block(self, id):
        trait_block = TraitBlock.objects.get(pk=id)
        data = {}
        trait = Trait.objects.get(pk=trait_block.trait_id)
        data['trait_title'] = trait.title
        data['id'] = trait_block.id
        data['trait_id'] = trait_block.trait_id
        data['kind'] = trait_block.kind
        data['position'] = trait_block.position
        data['title'] = trait_block.title
        data['sort_order'] = trait_block.sort_order
        if trait_block.kind == 'general_text':
            trait_block_version = TraitBlockVersion.objects.filter(trait_block_id=trait_block.id).filter(version_status='active').order_by('-created_at')
            if trait_block_version:
                data['title'] = trait_block_version[0].title
                data['text'] = trait_block_version[0].text
            else:
                data['title'] = 'No Version avaliable'
                data['text'] = 'No Version avaliable'
        if trait_block.kind == 'general_publications':
            publications = []
            trait_block_version = TraitBlockPublicationVersion.objects.filter(trait_block_id=trait_block.id).filter(version_status='active').order_by('-created_at')
            if trait_block_version:
                rows = TraitBlockPublication.objects.filter(trait_block_id=trait_block.id, trait_block_version_id=trait_block_version[0].id).all()
                for r in rows:
                    publications.append({
                        'id':         r.id,
                        'pmid':       r.pmid,
                        'doi':        r.doi,
                        'pmc':        r.pmc,
                        'title':      r.title,
                        'authors':    r.authors,
                        'journal':    r.journal
                    })
            data['publications'] = publications
        if trait_block.kind == 'general_alias':
            alias = []
            trait_block_version = TraitBlockAliasVersion.objects.filter(trait_block_id=trait_block.id).filter(version_status='active').order_by('-created_at')
            if trait_block_version:
                rows = TraitBlockAlias.objects.filter(trait_block_id=trait_block.id, trait_block_version_id=trait_block_version[0].id).all()
                for r in rows:
                    alias.append({
                        'alias':           r.alias,
                    })
            data['alias'] = alias
        return data
