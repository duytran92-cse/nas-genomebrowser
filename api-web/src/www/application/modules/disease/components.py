from application.models import *

class DataHelper(object):
    def load_associated_publications(self, id):
        data = Disease.objects.get(pk=id)
        # Get associtaed pubs
        publications = []
        rows = DiseaseAssociatedPublication.objects.filter(disease_id=data.id).all()
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

    def load_associated_genes(self, id):
        data = Disease.objects.get(pk=id)
        # Get associated genes
        genes = []
        rows = DiseaseAssociatedGene.objects.filter(disease_id=data.id).all()
        if rows:
            for r in rows:
                genes.append({
                    'id':           r.id,
                    'gene_name':    r.gene_name,
                })
        return genes
