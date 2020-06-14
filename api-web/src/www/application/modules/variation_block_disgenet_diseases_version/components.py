from application.models import *

class VariationBlockDisgenetDiseasesVersionHelper(object):
    def load_disgenet_diseases(self, id):
        disgenet_diseases = []
        rows = VariationBlockDisgenetDiseases.objects.filter(variation_block_version_id=id)
        if rows:
            for r in rows:
                disgenet_diseases.append({
                    'id':             r.id,
                    'pubmedid':       r.pubmedid,
                    'sentence':       r.sentence,
                    'title':          r.title
                })
        return disgenet_diseases
