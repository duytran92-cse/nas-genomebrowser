from application.models import *

class VariationBlockAliasVersionHelper(object):
    def load_alias(self, id):
        alias = []
        rows = VariationBlockAlias.objects.filter(variation_block_version_id=id)
        if rows:
            for r in rows:
                alias.append({
                    'id':         r.id,
                    'alias':      r.alias
                })
        return alias
