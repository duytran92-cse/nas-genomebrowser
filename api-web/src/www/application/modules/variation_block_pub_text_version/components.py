from application.models import *
class VariationBlockPublicationTextVersionHelper(object):
    def load_publication_text(self, id):
        publication_text = []
        rows = VariationBlockPublicationText.objects.filter(variation_block_version_id=id)
        if rows:
            for r in rows:
                publication_text.append({
                    'id':         r.id,
                    'pmid':       r.pmid,
                    'doi':        r.doi,
                    'pmc':        r.pmc,
                    'title':      r.title,
                    'authors':    r.authors,
                    'journal':    r.journal
                })
        return publication_text
