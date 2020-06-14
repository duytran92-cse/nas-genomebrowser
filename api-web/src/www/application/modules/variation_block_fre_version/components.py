from application.models import *

class VariationBlockFrequencyVersionHelper(object):
    def load_frequencies(self, id):
        frequencies = []
        rows = VariationBlockFrequency.objects.filter(variation_block_version_id=id)
        if rows:
            for r in rows:
                frequencies.append({
                    'id':                   r.id,
                    'popcode':              r.popcode,
                    'genotype_count_00':    r.genotype_count_00,
                    'genotype_count_01':    r.genotype_count_01,
                    'genotype_count_11':    r.genotype_count_11,
                })
        return frequencies
