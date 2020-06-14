from application.models import *

class GeneBlockAliasVersionHelper(object):
    def load_alias(self, id):
        alias = []
        rows = GeneBlockAlias.objects.filter(gene_block_version_id=id)
        if rows:
            for r in rows:
                alias.append({
                    'id':         r.id,
                    'alias':      r.alias
                })
        return alias
