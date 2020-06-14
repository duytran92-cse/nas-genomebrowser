from application.models import *

class DiseaseBlockAliasVersionHelper(object):
    def load_alias(self, id):
        alias = []
        rows = DiseaseBlockAlias.objects.filter(disease_block_version_id=id)
        if rows:
            for r in rows:
                alias.append({
                    'id':         r.id,
                    'alias':      r.alias
                })
        return alias
