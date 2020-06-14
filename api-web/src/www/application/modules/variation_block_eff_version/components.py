from application.models import *

class VariationBlockEffectVersionHelper(object):
    def load_risks(self, id):
        risks = []
        rows = VariationBlockEffect.objects.filter(variation_block_version_id=id)
        if rows:
            for r in rows:
                risks.append({
                    'id':           r.id,
                    'popcode':      r.popcode,
                    'genotype':     r.genotype,
                    'risk':         r.risk,
                    'odd_ratio':    r.odd_ratio,
                    'evidences':    r.evidences,
                    'pmid':         r.pmid
                })
        return risks
