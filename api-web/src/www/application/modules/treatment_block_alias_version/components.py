from application.models import *

class TreatmentBlockAliasVersionHelper(object):
    def load_alias(self, id):
        alias = []
        rows = TreatmentBlockAlias.objects.filter(treatment_block_version_id=id)
        if rows:
            for r in rows:
                alias.append({
                    'id':         r.id,
                    'alias':      r.alias
                })
        return alias
