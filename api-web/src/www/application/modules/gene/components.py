from application.models import *

class DataHelper(object):
    def load_associated_diseases(self, id):
        gene = Gene.objects.get(pk=id)
        # Get associated diseases
        diseases = []
        rows = GeneAssociatedDisease.objects.filter(gene_id=gene.id).all()
        if rows:
            for r in rows:
                diseases.append({
                    'id':               r.id,
                    'disease_name':     r.disease_name,
                })
        return diseases

    def load_associated_diseases_group_name(self, id):
        data = Gene.objects.get(pk=id)
        # Get associated diseases
        diseases = {}
        rows = GeneAssociatedDisease.objects.filter(gene_id=data.id).all()
        if rows:
            for r in rows:
                diseases[r.disease_name.strip(" ")] = {
                    'disease_name': r.disease_name
                }
        return diseases

    def load_associated_publications(self, id):
        gene = Gene.objects.get(pk=id)
        # Get associated diseases
        publications = []
        rows = GeneAssociatedPublication.objects.filter(gene_id=gene.id).all()
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
