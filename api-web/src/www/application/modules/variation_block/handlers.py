from notasquare.urad_api import *
from application.models import *
from application import constants
from . import components
import requests

class List(handlers.standard.ListHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('variation_id', 'integer'):
            self.add_error('variation_id', 'INVALID_DATA')
        return parser.get_data()
    def create_query(self, data):
        query = VariationBlock.objects
        query = query.filter(variation_id=data['variation_id'])
        query = query.filter(is_disabled=False)
        if 'kind' in data:
            if data['kind'] != '':
                query = query.filter(kind=data['kind'])
        if 'title' in data:
            query = query.filter(title__contains=data['text'])
        return query
    def serialize_entry(self, variation_block):
        # Get active and latest version
        if variation_block.kind == 'general_text':
            query = VariationBlockVersion.objects.filter(variation_block_id=variation_block.id, version_status='active', is_disabled=False)
        elif variation_block.kind == 'general_alias':
            query = VariationBlockAliasVersion.objects.filter(variation_block_id=variation_block.id, version_status='active', is_disabled=False)
        elif variation_block.kind == 'general_publications':
            query = VariationBlockPublicationVersion.objects.filter(variation_block_id=variation_block.id, version_status='active', is_disabled=False)
        elif variation_block.kind == 'variation_infobox':
            query = VariationBlockInfoboxVersion.objects.filter(variation_block_id=variation_block.id, version_status='active', is_disabled=False)
        elif variation_block.kind == 'variation_effect':
            query = VariationBlockEffectVersion.objects.filter(variation_block_id=variation_block.id, version_status='active', is_disabled=False)
        elif variation_block.kind == 'variation_frequency':
            query = VariationBlockFrequencyVersion.objects.filter(variation_block_id=variation_block.id, version_status='active', is_disabled=False)
        elif variation_block.kind == 'general_disgenet_diseases':
            query = VariationBlockDisgenetDiseasesVersion.objects.filter(variation_block_id=variation_block.id, version_status='active', is_disabled=False)
        elif variation_block.kind == 'variation_pub_text':
            query = VariationBlockPublicationTextVersion.objects.filter(variation_block_id=variation_block.id, version_status='active', is_disabled=False)

        active_version = query.filter(is_stable=True).order_by('-created_at')[:1]
        latest_version = query.order_by('-created_at')[:1]
        l_ver = 0
        ac_ver = 0
        if latest_version.first():
            l_ver = latest_version.first().version

        if active_version.first():
            ac_ver = active_version.first().version

        return {
            'id': variation_block.id,
            'title': variation_block.title,
            'text': variation_block.text,
            'kind': variation_block.kind,
            'position': variation_block.position,
            'sort_order': variation_block.sort_order,
            'variation': variation_block.variation_id,
            'active_version': ac_ver,
            'latest_version': l_ver
        }

class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        return components.VariationBlockHelper().load_variation_block(data['id'])

class Create(handlers.standard.CreateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('variation_id', 'integer'):
            self.add_error('variation_id', 'INVALID_DATA')
        if not parser.parse('kind', 'string'):
            self.add_error('kind', 'MUST_NOT_BE_EMPTY')
        if not parser.parse('position', 'string'):
            self.add_error('position', 'MUST_NOT_BE_EMPTY')
        if not parser.parse('title', 'string'):
            self.add_error('title', 'MUST_NOT_BE_EMPTY')
        if 'sort_order' in params:
            if not parser.parse('sort_order', 'integer'):
                self.add_error('sort_order', 'MUST_NOT_BE_EMPTY')
        return parser.get_data()
    def create(self, data):
        variation_block = VariationBlock()
        variation_block.variation_id = data['variation_id']
        variation_block.kind = data['kind']
        variation_block.position = data['position']
        variation_block.title = data['title']
        if 'sort_order' in data:
            variation_block.sort_order = data['sort_order']
        variation_block.save()

        return variation_block


class Update(handlers.standard.UpdateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('id', 'integer'):
            self.add_error('id', 'MUST_NOT_BE_EMPTY')
        if 'position' in params:
            if not parser.parse('position', 'string'):
                self.add_error('position', 'MUST_NOT_BE_EMPTY')
        if 'title' in params:
            if not parser.parse('title', 'string'):
                self.add_error('title', 'MUST_NOT_BE_EMPTY')
        if 'sort_order' in params:
            if not parser.parse('sort_order', 'integer'):
                self.add_error('sort_order', 'MUST_NOT_BE_EMPTY')

        variation_block = VariationBlock.objects.get(pk=params['id'])
        if variation_block.kind == 'general_publications':
            pass
        if variation_block.kind == 'variation_effect':
            pass
        if variation_block.kind == 'general_disgenet_diseases':
            pass

        return parser.get_data()
    def update(self, data):
        print data

        variation_block = VariationBlock.objects.get(pk=data['id'])
        variation = Variation.objects.get(pk=variation_block.variation_id)
        if 'position' in data:
            variation_block.position = data['position']
        if 'title' in data:
            variation_block.title = data['title']
        if 'sort_order' in data:
            variation_block.sort_order = data['sort_order']
        if 'text' in data:
            variation_block.text = data['text']
        variation_block.save()

        if variation_block.kind == 'general_text':
            variation_block_version = VariationBlockVersion()
            variation_block_version.variation_block_id = variation_block.id
            variation_block_version.variation_id = variation.id
            variation_block_version.title = data['title']
            variation_block_version.text = data['text']
            # Set status active
            variation_block_version.version_status = 'active'
            if 'verify' in data:
                variation_block_version.is_stable = True
            variation_block_version.author = 'anonymous' # Fix me
            # Set version
            version = VariationBlockVersion.objects.filter(variation_id=variation.id, variation_block_id=variation_block.id).aggregate(Max('version'))
            if version['version__max']:
                variation_block_version.version = int(version['version__max']) + 1
            variation_block_version.save()

        if variation_block.kind == 'variation_pub_text':
            variation_block_pub_text_version = VariationBlockPublicationTextVersion()
            variation_block_pub_text_version.variation_block_id = variation_block.id
            variation_block_pub_text_version.variation_id = variation.id
            variation_block_pub_text_version.title = ''

            # Set status active
            variation_block_pub_text_version.version_status = 'active'
            if 'verify' in data:
                variation_block_pub_text_version.is_stable = True
            variation_block_pub_text_version.author = 'anonymous' # Fix me
            # Set version
            version = VariationBlockPublicationTextVersion.objects.filter(variation_id=variation.id, variation_block_id=variation_block.id).aggregate(Max('version'))
            if version['version__max']:
                variation_block_pub_text_version.version = int(version['version__max']) + 1
            variation_block_pub_text_version.save()

            ## Save Block
            for val in data['pub_text']:
                variation_block_publication_text = VariationBlockPublicationText()
                variation_block_publication_text.variation_block_id = variation_block.id
                variation_block_publication_text.variation_block_version_id = variation_block_pub_text_version.id
                variation_block_publication_text.sentence = val['sentence']
                variation_block_publication_text.title    = val['title']
                variation_block_publication_text.pubmedid = val['pubmedid']
                variation_block_publication_text.save()

        if variation_block.kind == 'general_publications':
            # VariationBlockPublication.objects.filter(variation_block_id=variation_block.id).delete()
            # if 'new_version' in data:
            variation_block_pub_version = VariationBlockPublicationVersion()
            variation_block_pub_version.variation_id = variation.id
            variation_block_pub_version.variation_block_id = variation_block.id
            # Set status active
            variation_block_pub_version.version_status = 'active'
            if 'verify' in data:
                variation_block_pub_version.is_stable = True
            variation_block_pub_version.author = 'anonymous' # Fix me
            # Set version
            version = VariationBlockPublicationVersion.objects.filter(variation_id=variation.id, variation_block_id=variation_block.id).aggregate(Max('version'))
            if version['version__max']:
                variation_block_pub_version.version = int(version['version__max']) + 1
            variation_block_pub_version.save()

            for publication in data['publications']:
                variation_block_publication = VariationBlockPublication()
                variation_block_publication.variation_block_id = variation_block.id
                variation_block_publication.variation_block_version_id = variation_block_pub_version.id
                variation_block_publication.pmid = publication['pmid']
                variation_block_publication.doi = publication['doi']
                variation_block_publication.pmc = publication['pmc']
                variation_block_publication.title = publication['title']
                variation_block_publication.authors = publication['authors']
                variation_block_publication.journal = publication['journal']
                variation_block_publication.save()

        if variation_block.kind == 'general_disgenet_diseases':
            # VariationBlockDisgenetDiseases.objects.filter(variation_block_id=variation_block.id).delete()
            # if 'new_version' in data:
            variation_block_disgenet_diseases_version = VariationBlockDisgenetDiseasesVersion()
            variation_block_disgenet_diseases_version.variation_id = variation.id
            variation_block_disgenet_diseases_version.variation_block_id = variation_block.id
            # Set status active
            variation_block_disgenet_diseases_version.version_status = 'active'
            if 'verify' in data:
                variation_block_disgenet_diseases_version.is_stable = True
            variation_block_disgenet_diseases_version.author = 'anonymous' # Fix me
            # Set version
            version = VariationBlockDisgenetDiseasesVersion.objects.filter(variation_id=variation.id, variation_block_id=variation_block.id).aggregate(Max('version'))
            if version['version__max']:
                variation_block_disgenet_diseases_version.version = int(version['version__max']) + 1
            variation_block_disgenet_diseases_version.save()

            for disgenet_diseases in data['disgenet_diseases']:
                variation_block_disgenet_diseases = VariationBlockDisgenetDiseases()
                variation_block_disgenet_diseases.variation_block_id = variation_block.id
                variation_block_disgenet_diseases.variation_block_version_id = variation_block_disgenet_diseases_version.id
                variation_block_disgenet_diseases.pubmedid = disgenet_diseases['pubmedid']
                variation_block_disgenet_diseases.title = disgenet_diseases['title']
                variation_block_disgenet_diseases.save()

        if variation_block.kind == 'variation_effect':
            variation_block_eff_version = VariationBlockEffectVersion()
            variation_block_eff_version.variation_block_id = variation_block.id
            variation_block_eff_version.variation_id = variation.id
            # Set status active
            variation_block_eff_version.version_status = 'active'
            if 'verify' in data:
                variation_block_eff_version.is_stable = True
            variation_block_eff_version.author = 'anonymous' # Fix me
            # Set version
            version = VariationBlockEffectVersion.objects.filter(variation_id=variation.id, variation_block_id=variation_block.id).aggregate(Max('version'))
            if version['version__max']:
                variation_block_eff_version.version = int(version['version__max']) + 1
            variation_block_eff_version.save()

            # VariationBlockEffect.objects.filter(variation_block_id=variation_block.id).delete()
            for risk in data['risks']:
                variation_block_effect_risk = VariationBlockEffect()
                variation_block_effect_risk.variation_block_id = variation_block.id
                variation_block_effect_risk.variation_block_version_id = variation_block_eff_version.id
                variation_block_effect_risk.popcode = risk['popcode']
                variation_block_effect_risk.genotype = risk['genotype']
                variation_block_effect_risk.risk = risk['risk']
                variation_block_effect_risk.odd_ratio = risk['odd_ratio']
                variation_block_effect_risk.evidences = risk['evidences']
                variation_block_effect_risk.pmid = risk['pmid']
                variation_block_effect_risk.save()

            if 'genotypes' in data:
                VariationGenotype.objects.filter(variation_id=variation.id).delete()
                for genotype in data['genotypes']:
                    if genotype.get('source', '') != '' and requests.head(genotype['source']).status_code != '403' and requests.head(genotype['source']).status_code != '404':
                        variation_genotype = VariationGenotype()
                        variation_genotype.genotype = genotype['genotype_eff']
                        variation_genotype.box_color = genotype['box_color']
                        variation_genotype.source = genotype['source']
                        variation_genotype.variation_id = variation.id
                        variation_genotype.save()

        if variation_block.kind == 'general_alias':
            variation_alias_version = VariationBlockAliasVersion()
            variation_alias_version.variation_id = variation.id
            variation_alias_version.variation_block_id = variation_block.id
            # Set status active
            variation_alias_version.version_status = 'active'
            if 'verify' in data:
                variation_alias_version.is_stable = True
            variation_alias_version.author = 'anonymous' # Fix me
            # Set version
            version = VariationBlockAliasVersion.objects.filter(variation_id=variation.id, variation_block_id=variation_block.id).aggregate(Max('version'))
            if version['version__max']:
                variation_alias_version.version = int(version['version__max']) + 1
            variation_alias_version.save()

            for item in data['alias']:
                variation_block_alias = VariationBlockAlias()
                variation_block_alias.variation_block_id = variation_block.id
                variation_block_alias.variation_block_version_id = variation_alias_version.id
                variation_block_alias.alias = item['alias']
                variation_block_alias.save()

        if variation_block.kind == 'variation_frequency':
            variation_block_fre_version = VariationBlockFrequencyVersion()
            variation_block_fre_version.variation_id = variation.id
            variation_block_fre_version.variation_block_id = variation_block.id
            # Set status active
            variation_block_fre_version.version_status = 'active'
            if 'verify' in data:
                variation_block_fre_version.is_stable = True
            variation_block_fre_version.author = 'anonymous' # Fix me
            # Set version
            version = VariationBlockFrequencyVersion.objects.filter(variation_id=variation.id, variation_block_id=variation_block.id).aggregate(Max('version'))
            if version['version__max']:
                variation_block_fre_version.version = int(version['version__max']) + 1
            variation_block_fre_version.save()

            for item in data['frequencies']:
                variation_block_fre = VariationBlockFrequency()
                variation_block_fre.variation_block_id = variation_block.id
                variation_block_fre.variation_block_version_id = variation_block_fre_version.id
                variation_block_fre.popcode = item['popcode']
                variation_block_fre.genotype_count_00 = item['genotype_count_00']
                variation_block_fre.genotype_count_01 = item['genotype_count_01']
                variation_block_fre.genotype_count_11 = item['genotype_count_11']
                variation_block_fre.save()

        if variation_block.kind == 'variation_infobox':
            variation_block_infobox_version = VariationBlockInfoboxVersion()
            variation_block_infobox_version.variation_id = variation.id
            variation_block_infobox_version.variation_block_id = variation_block.id
            # Set status active
            variation_block_infobox_version.version_status = 'active'
            if 'verify' in data:
                variation_block_infobox_version.is_stable = True
            variation_block_infobox_version.author = 'anonymous' # Fix me
            # Set version
            version = VariationBlockInfoboxVersion.objects.filter(variation_id=variation.id, variation_block_id=variation_block.id).aggregate(Max('version'))
            if version['version__max']:
                variation_block_infobox_version.version = int(version['version__max']) + 1
            variation_block_infobox_version.save()

            for item in data['infobox']:
                variation_block_infobox = VariationBlockInfobox()
                variation_block_infobox.variation_block_id = variation_block.id
                variation_block_infobox.variation_block_version_id = variation_block_infobox_version.id
                variation_block_infobox.key = item['key']
                variation_block_infobox.value = item['value']
                variation_block_infobox.save()

        return variation_block


class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        variation_block = VariationBlock.objects.get(pk=data['id'])
        variation_block.is_disabled = True
        variation_block.save()
        return 1

class SaveTextEff(handlers.standard.UpdateHandler):
    def update(self, data):
        query = VariationEffectNote.objects.filter()
        if query:
            note = query[0]
        else:
            note = VariationEffectNote()
        if 'key' in data:
            if data['key'] == 'genotype':
                note.genotype = data.get('text', '')
            if data['key'] == 'popcode':
                note.popcode = data.get('text', '')
            if data['key'] == 'risk':
                note.risk = data.get('text', '')
            if data['key'] == 'odd_ratio':
                note.odd_ratio = data.get('text', '')
            if data['key'] == 'evidences':
                note.evidences = data.get('text', '')
            if data['key'] == 'pmid':
                note.pmid = data.get('text', '')
        note.save()
        return note

class Helper(handlers.standard.GetHandler):
    def get_data(self, data):
        variation_block = VariationBlock.objects.get(pk=data['id'])
        variation = Variation.objects.get(pk=variation_block.variation_id)
        return {
            'title': variation.title
        }
