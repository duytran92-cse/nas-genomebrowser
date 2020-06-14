from application.models import *

class TraitBlockAliasVersionHelper(object):
    def load_alias(self, id):
        alias = []
        rows = TraitBlockAlias.objects.filter(trait_block_version_id=id)
        if rows:
            for r in rows:
                alias.append({
                    'id':         r.id,
                    'alias':      r.alias
                })
        return alias
