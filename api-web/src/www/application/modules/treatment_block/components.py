
from application.models import *

class TreatmentBlockHelper(object):
    def load_treatment_block(self, id):
        treatment_block = TreatmentBlock.objects.get(pk=id)
        data = {}
        treatment = Treatment.objects.get(pk=treatment_block.treatment_id)
        data['treatment_title'] = treatment.title
        data['id'] = treatment_block.id
        data['treatment_id'] = treatment_block.treatment_id
        data['kind'] = treatment_block.kind
        data['position'] = treatment_block.position
        data['title'] = treatment_block.title
        data['sort_order'] = treatment_block.sort_order
        if treatment_block.kind == 'general_text':
            treatment_block_version = TreatmentBlockVersion.objects.filter(treatment_block_id=treatment_block.id).filter(version_status='active').order_by('-created_at')
            if treatment_block_version:
                data['title'] = treatment_block_version[0].title
                data['text'] = treatment_block_version[0].text
            else:
                data['title'] = 'No Version avaliable'
                data['text'] = 'No Version avaliable'
        if treatment_block.kind == 'general_publications':
            publications = []
            treatment_block_version = TreatmentBlockPublicationVersion.objects.filter(treatment_block_id=treatment_block.id).filter(version_status='active').order_by('-created_at')
            if treatment_block_version:
                rows = TreatmentBlockPublication.objects.filter(treatment_block_id=treatment_block.id, treatment_block_version_id=treatment_block_version[0].id).all()
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
        if treatment_block.kind == 'general_alias':
            alias = []
            treatment_block_version = TreatmentBlockAliasVersion.objects.filter(treatment_block_id=treatment_block.id).filter(version_status='active').order_by('-created_at')
            if treatment_block_version:
                rows = TreatmentBlockAlias.objects.filter(treatment_block_id=treatment_block.id, treatment_block_version_id=treatment_block_version[0].id).all()
                for r in rows:
                    alias.append({
                        'alias':           r.alias,
                    })
            data['alias'] = alias
        return data
