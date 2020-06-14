from application.models import *

class GeneBlockEffectVersionHelper(object):
    def load_effects(self, id):
        effects = []
        rows = GeneBlockEffect.objects.filter(gene_block_version_id=id)
        if rows:
            for r in rows:
                effects.append({
                    'id':           r.id,
                    'type':         r.type,
                    'effect':       r.effect,
                    'evidences':    r.evidences,
                    'publications': r.publication
                })
        return effects
