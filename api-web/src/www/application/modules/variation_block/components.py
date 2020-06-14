
from application.models import *
from application import constants
from application.modules.variation import components

class VariationBlockHelper(object):
    def get_pop_name(self, popcode):
        name = ''
        for pop in constants.POPULATION_CODES:
            if pop['id'] == popcode:
                name = pop['label']
        return name
    def count_per(self, val_1, val_2, val_3, total):
        fre_1 = int(round((float(val_1)/float(total))*100,0))
        fre_2 = int(round((float(val_2)/float(total))*100,0))
        fre_3 = int(round((float(val_3)/float(total))*100,0))
        if (fre_1 + fre_2 + fre_3) > 100:
            if fre_1 > fre_2 and fre_1 > fre_3:
                fre_1 = 100- (fre_3+ fre_2)
            if fre_2 > fre_1 and fre_2 > fre_3:
                fre_2 = 100- (fre_1+fre_3)
            if fre_3 > fre_2 and fre_3 > fre_1:
                fre_3 = 100- (fre_1+fre_2)
        return [fre_1, fre_2, fre_3]

    def load_variation_block(self, id, filter_val = 'Global'):
        variation_block = VariationBlock.objects.get(pk=id)
        data = {}
        variation = Variation.objects.get(pk=variation_block.variation_id)
        data['variation_title'] = variation.title

        data['id'] = variation_block.id
        data['variation_id'] = variation_block.variation_id
        data['kind'] = variation_block.kind
        data['position'] = variation_block.position
        data['title'] = variation_block.title
        data['sort_order'] = variation_block.sort_order
        if variation_block.kind == 'general_text':
            variation_block_version = VariationBlockVersion.objects.filter(variation_block_id=variation_block.id).filter(version_status='active').order_by('-created_at')
            if variation_block_version:
                data['title'] = variation_block_version[0].title
                data['text'] = variation_block_version[0].text
            else:
                data['title'] = 'No Version avaliable'
                data['text'] = 'No Version avaliable'
        if variation_block.kind == 'general_publications':
            publications = []
            variation_block_version = VariationBlockPublicationVersion.objects.filter(variation_block_id=variation_block.id).filter(version_status='active').order_by('-created_at')
            if variation_block_version:
                rows = VariationBlockPublication.objects.filter(variation_block_id=variation_block.id, variation_block_version_id=variation_block_version[0].id).all()
                for r in rows:
                    publications.append({
                        'id':         r.id,
                        'pmid':       r.pmid,
                        'doi':        r.doi,
                        'pmc':        r.pmc,
                        'title':      r.title,
                        'authors':    r.authors,
                        'journal':    r.journal
                    })
            data['publications'] = publications
        if variation_block.kind == 'variation_effect':
            risks = []
            variation_block_version = VariationBlockEffectVersion.objects.filter(variation_block_id=variation_block.id).filter(version_status='active').order_by('-created_at')
            if variation_block_version:
                if filter_val == 'None' or filter_val == 'Global':
                    rows = VariationBlockEffect.objects.filter(variation_block_id=variation_block.id, variation_block_version_id=variation_block_version[0].id).all()
                else:
                    rows = VariationBlockEffect.objects.filter(popcode= filter_val, variation_block_id=variation_block.id, variation_block_version_id=variation_block_version[0].id).all()
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

            data['risks'] = risks
            data['filter'] = filter_val
            helper = components.DataHelper()
            data['genotypes'] = helper.load_genotypes(variation.id)
        if variation_block.kind == 'general_alias':
            alias = []
            variation_block_version = VariationBlockAliasVersion.objects.filter(variation_block_id=variation_block.id).filter(version_status='active').order_by('-created_at')
            if variation_block_version:
                rows = VariationBlockAlias.objects.filter(variation_block_id=variation_block.id, variation_block_version_id=variation_block_version[0].id).all()
                for r in rows:
                     alias.append({
                        'alias':           r.alias,
                    })
            data['alias'] = alias
        if variation_block.kind == 'variation_infobox':
            infobox = []
            variation_block_version = VariationBlockInfoboxVersion.objects.filter(variation_block_id=variation_block.id).filter(version_status='active').order_by('-created_at')
            if variation_block_version:
                rows = VariationBlockInfobox.objects.filter(variation_block_id=variation_block.id, variation_block_version_id=variation_block_version[0].id).all()
                for r in rows:
                    infobox.append({
                        'key':          r.key,
                        'value':        r.value
                    })
            data['infobox'] = infobox

        if variation_block.kind == 'general_disgenet_diseases':
            disgenet_diseases = []
            arr_dis = {}
            variation_block_version = VariationBlockDisgenetDiseasesVersion.objects.filter(variation_block_id=variation_block.id).filter(version_status='active').order_by('-created_at')
            if variation_block_version:
                rows = VariationBlockDisgenetDiseases.objects.filter(variation_block_id=variation_block.id, variation_block_version_id=variation_block_version[0].id).all()
                for r in rows:
                    if r.title.strip(" ") in arr_dis:
                        arr_dis[r.title.strip(" ")]['data'].append({
                            'id':              r.id,
                            'title':           r.title,
                            'pubmedid':        r.pubmedid,
                            'sentence':        r.sentence,
                        })
                    else:
                        arr_dis[r.title.strip(" ")] = {
                            'title':           r.title,
                            'data':            [{
                                'id':              r.id,
                                'title':           r.title,
                                'pubmedid':        r.pubmedid,
                                'sentence':        r.sentence,
                            }]
                        }
                    disgenet_diseases.append({
                        'id':              r.id,
                        'title':           r.title,
                        'pubmedid':        r.pubmedid,
                        'sentence':        r.sentence,
                    })
            data['disgenet_diseases'] = disgenet_diseases
            data['disgenet_show']     = arr_dis
        if variation_block.kind == 'variation_pub_text':
            pub_text = []
            variation_block_version = VariationBlockPublicationTextVersion.objects.filter(variation_block_id=variation_block.id).filter(version_status='active').order_by('-created_at')
            if variation_block_version:
                rows = VariationBlockPublicationText.objects.filter(variation_block_id=variation_block.id, variation_block_version_id=variation_block_version[0].id).all()
                for r in rows:
                    pub_text.append({
                        'id':              r.id,
                        'title':           r.title,
                        'pubmedid':        r.pubmedid,
                        'sentence':        r.sentence,
                    })
            data['pub_text'] = pub_text
        if variation_block.kind == 'variation_frequency':
            frequencies = []
            frequencies_sub = []
            variation_block_version = VariationBlockFrequencyVersion.objects.filter(variation_block_id=variation_block.id).filter(version_status='active').order_by('-created_at')
            if variation_block_version:

                ## frequencies for admin
                rows = VariationBlockFrequency.objects.filter(variation_block_id=variation_block.id, variation_block_version_id=variation_block_version[0].id).all()
                for r in rows:
                    count_type = 0
                    if r.genotype_count_00 != 0:
                        count_type = count_type + 1
                    if r.genotype_count_01 != 0:
                        count_type = count_type + 1
                    if r.genotype_count_11 != 0:
                        count_type = count_type + 1
                    frequencies.append({
                        'popcode':              r.popcode,
                        'name':                 self.get_pop_name(r.popcode),
                        'genotype_count_00':    r.genotype_count_00,
                        'genotype_count_01':    r.genotype_count_01,
                        'genotype_count_11':    r.genotype_count_11,
                        'total':                int(r.genotype_count_00) + int(r.genotype_count_01) + int(r.genotype_count_11),
                        'count_type':           count_type
                    })

                ## frequencies for front (POP & SUB_POP) --> duplicate
                pops = constants.SUB_POPULATION_CODES
                for val in pops:
                    rows = VariationBlockFrequency.objects.filter(variation_block_id=variation_block.id, variation_block_version_id=variation_block_version[0].id, popcode=val).all()
                    sub = []
                    for r in rows:
                        count_type = 0
                        if r.genotype_count_00 != 0:
                            count_type = count_type + 1
                        if r.genotype_count_01 != 0:
                            count_type = count_type + 1
                        if r.genotype_count_11 != 0:
                            count_type = count_type + 1

                        ## for each SUB POP
                        for sub_pop in pops[val]:
                            rows_sub = VariationBlockFrequency.objects.filter(variation_block_id=variation_block.id, variation_block_version_id=variation_block_version[0].id, popcode=sub_pop['id']).all()
                            for r_sub in rows_sub:
                                count_type_sub = 0
                                if r_sub.genotype_count_00 != 0:
                                    count_type_sub = count_type_sub + 1
                                if r_sub.genotype_count_01 != 0:
                                    count_type_sub = count_type_sub + 1
                                if r_sub.genotype_count_11 != 0:
                                    count_type_sub = count_type_sub + 1
                                total = int(r_sub.genotype_count_00) + int(r_sub.genotype_count_01) + int(r_sub.genotype_count_11)
                                percent = self.count_per(r_sub.genotype_count_00, r_sub.genotype_count_01, r_sub.genotype_count_11, total)
                                sub.append({
                                    'popcode': r_sub.popcode,
                                    'name':                 self.get_pop_name(r_sub.popcode),
                                    'genotype_count_00':    r_sub.genotype_count_00,
                                    'per_00':               percent[0],
                                    'per_01':               percent[1],
                                    'per_11':               percent[2],
                                    'genotype_count_01':    r_sub.genotype_count_01,
                                    'genotype_count_11':    r_sub.genotype_count_11,
                                    'total':                total,
                                    'count_type':           count_type_sub,
                                })

                        total = int(r.genotype_count_00) + int(r.genotype_count_01) + int(r.genotype_count_11)
                        percent = self.count_per(r.genotype_count_00, r.genotype_count_01, r.genotype_count_11, total)

                        frequencies_sub.append({
                            'popcode':              r.popcode,
                            'name':                 self.get_pop_name(r.popcode),
                            'genotype_count_00':    r.genotype_count_00,
                            'genotype_count_01':    r.genotype_count_01,
                            'genotype_count_11':    r.genotype_count_11,
                            'total':                total,
                            'per_00':               percent[0],
                            'per_01':               percent[1],
                            'per_11':               percent[2],
                            'count_type':           count_type,
                            'sub':                  sub
                        })
            data['frequencies'] = frequencies
            data['frequencies_front'] = frequencies_sub
        return data
