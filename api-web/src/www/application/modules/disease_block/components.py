
from application.models import *

class DiseaseBlockHelper(object):
    def load_disease_block(self, id):
        disease_block = DiseaseBlock.objects.get(pk=id)
        data = {}
        disease = Disease.objects.get(pk=disease_block.disease_id)
        data['disease_title'] = disease.title
        data['id'] = disease_block.id
        data['disease_id'] = disease_block.disease_id
        data['kind'] = disease_block.kind
        data['position'] = disease_block.position
        data['title'] = disease_block.title
        data['sort_order'] = disease_block.sort_order
        if disease_block.kind == 'general_text':
            disease_block_version = DiseaseBlockVersion.objects.filter(disease_block_id=disease_block.id).filter(version_status='active').order_by('-created_at')
            if disease_block_version:
                data['title'] = disease_block_version[0].title
                data['text'] = disease_block_version[0].text
            else:
                data['title'] = 'No Version avaliable'
                data['text'] = 'No Version avaliable'
        if disease_block.kind == 'general_publications':
            publications = []
            disease_block_version = DiseaseBlockPublicationVersion.objects.filter(disease_block_id=disease_block.id).filter(version_status='active').order_by('-created_at')
            if disease_block_version:
                rows = DiseaseBlockPublication.objects.filter(disease_block_id=disease_block.id, disease_block_version_id=disease_block_version[0].id).all()
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
        if disease_block.kind == 'general_alias':
            alias = []
            disease_block_version = DiseaseBlockAliasVersion.objects.filter(disease_block_id=disease_block.id).filter(version_status='active').order_by('-created_at')
            if disease_block_version:
                rows = DiseaseBlockAlias.objects.filter(disease_block_id=disease_block.id, disease_block_version_id=disease_block_version[0].id).all()
                for r in rows:
                    alias.append({
                        'alias':           r.alias,
                    })
            data['alias'] = alias
        return data
