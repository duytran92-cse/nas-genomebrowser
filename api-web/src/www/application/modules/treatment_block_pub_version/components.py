from application.models import *

class TreatmentBlockPublicationVersionHelper(object):
    def load_publications(self, id):
        publications = []
        rows = TreatmentBlockPublication.objects.filter(treatment_block_version_id=id)
        if rows:
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
        return publications
