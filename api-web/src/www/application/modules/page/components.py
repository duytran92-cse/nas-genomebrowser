from application.models import *

class PageHelper(object):
    def load_associated_publications(self, id):
        page = Page.objects.get(pk=id)
        # Get associtaed pubs
        publications = []
        rows = PageAssociatedPublication.objects.filter(page_id=page.id).all()
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
        page = Page.objects.get(pk=id)
        # Get associated genes
        genes = []
        rows = PageAssociatedGene.objects.filter(page_id=page.id).all()
        if rows:
            for r in rows:
                genes.append({
                    'id':           r.id,
                    'gene_name':    r.gene_name,
                })
        return genes

    def load_associated_diseases(self, id):
        page = Page.objects.get(pk=id)
        # Get associated diseases
        diseases = []
        rows = PageAssociatedDisease.objects.filter(page_id=page.id).all()
        if rows:
            for r in rows:
                diseases.append({
                    'id':               r.id,
                    'disease_name':     r.disease_name,
                })
        return diseases
