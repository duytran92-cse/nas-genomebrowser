from application.models import *

class DataHelper(object):
    def load_associated_publications(self, id):
        data = Variation.objects.get(pk=id)
        # Get associtaed pubs
        publications = []
        rows = VariationAssociatedPublication.objects.filter(variation_id=data.id).all()
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
        data = Variation.objects.get(pk=id)
        # Get associated genes
        genes = []
        rows = VariationAssociatedGene.objects.filter(variation_id=data.id).all()
        if rows:
            for r in rows:
                genes.append({
                    'id':           r.id,
                    'gene_name':    r.gene_name,
                })
        return genes

    def load_associated_diseases(self, id):
        data = Variation.objects.get(pk=id)
        # Get associated diseases
        diseases = []
        rows = VariationAssociatedDisease.objects.filter(variation_id=data.id).all()
        if rows:
            for r in rows:
                diseases.append({
                    'id':           r.id,
                    'disease_name':    r.disease_name,
                })
        return diseases

    def load_associated_diseases_group_name(self, id):
        data = Variation.objects.get(pk=id)
        # Get associated diseases
        diseases = {}
        rows = VariationAssociatedDisease.objects.filter(variation_id=data.id).all()
        if rows:
            for r in rows:
                diseases[r.disease_name.strip(" ")] = {
                    'disease_name': r.disease_name
                }
        return diseases

    def load_genotypes(self, id):
        data = Variation.objects.get(pk=id)
        genotypes = []
        rows = VariationGenotype.objects.filter(variation_id=data.id).all()
        if rows:
            for r in rows:
                genotypes.append({
                    'id':          r.id,
                    'genotype':    r.genotype,
                    'box_color':   r.box_color,
                    'source':      r.source,
                    'genotype_eff':r.genotype
                })
        return genotypes

    def load_note_eff(self, id):
        query = VariationEffectNote.objects.filter()
        data = []
        if query:
            r = query[0]
            data = {
                'popcode':      r.popcode,
                'genotype':     r.genotype,
                'risk':         r.risk,
                'odd_ratio':    r.odd_ratio,
                'evidences':    r.evidences,
                'pmid':         r.pmid
            }
        return data
