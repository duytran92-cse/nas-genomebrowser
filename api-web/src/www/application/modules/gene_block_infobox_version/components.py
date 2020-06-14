from application.models import *

class GeneBlockInfoboxVersionHelper(object):
    def load_infobox(self, id):
        infobox = []
        rows = GeneBlockInfobox.objects.filter(gene_block_version_id=id)
        if rows:
            for r in rows:
                infobox.append({
                    'id':               r.id,
                    'description':      r.description,
                    'chromosome':       r.chromosome,
                    'start':            r.start,
                    'end':              r.end,
                    'number_of_exons':  r.number_of_exons,
                    'protein_products': r.protein_products
                })
        return infobox
