from application.models import *

class VariationBlockInfoboxVersionHelper(object):
    def load_infobox(self, id):
        infobox = []
        rows = VariationBlockInfobox.objects.filter(variation_block_version_id=id)
        if rows:
            for r in rows:
                infobox.append({
                    'id':        r.id,
                    'key':       r.key,
                    'value':     r.value,
                })
        return infobox
