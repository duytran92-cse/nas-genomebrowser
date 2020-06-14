import json, pika, os
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from notasquare.urad_api.containers.standard import Container
from application.models import *
from django.conf import settings

class Command(BaseCommand):
    def consume_local(self, ch, method, properties, body):
        record = json.loads(body)
        for record in json.loads(body):  ## <======== Local
            data = []
            data = record
            data.update(record['core_attributes'])
            data.pop('core_attributes')
            self.generate_variation(data)

            print "="*10+ "=> Generate variation " + data['rsnumber'] + " => Done"
        print "[*] To exit press CTRL+C"

    def consume(self, ch, method, properties, body):
        record = json.loads(body)
        data = []
        data = record
        data.update(record['core_attributes'])
        data.pop('core_attributes')
        self.generate_variation(data)

        print "="*10+ "=> Generate variation " + data['rsnumber'] + " => Done"
        print "[*] To exit press CTRL+C"

    def handle(self, *args, **kwargs):
        print "[x] RECEIVING DATA"

        credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASS)
        connection = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBITMQ_HOST, settings.RABBITMQ_PORT, '/', credentials))

        channel = connection.channel()
        # channel.queue_declare(queue=settings.GENODATA_QUEUE_VARIATION, durable=True) ## <=== Local
        channel.queue_declare(queue=settings.GENODATA_QUEUE_VARIATION)

        print "[*] Waiting for data. To exit press CTRL+C"


        # channel.basic_consume(self.consume_local, queue=settings.GENODATA_QUEUE_VARIATION, no_ack=True) ## <=== Local
        channel.basic_consume(self.consume, queue=settings.GENODATA_QUEUE_VARIATION, no_ack=True)
        channel.start_consuming()

    ## ====================================================================
    ## Variation
    def generate_variation(self, variation_record):
        if variation_record.get('allele_string', '') != '':
            arr_allele = variation_record['allele_string'].split('/')
            if len(arr_allele) == 2:
                rsnumber = variation_record['rsnumber']
                query = Variation.objects.filter(title = rsnumber)
                if query.count() == 0:
                    variation = Variation()
                    variation.title = rsnumber
                    variation.save()

                    ## Add new Genotype ##

                    type_1 = arr_allele[0]+ "/"+ arr_allele[0]
                    type_2 = arr_allele[0]+ "/"+ arr_allele[1]
                    type_3 = arr_allele[1]+ "/"+ arr_allele[1]

                    genotype_1 = VariationGenotype()
                    genotype_1.genotype = type_1
                    genotype_1.box_color = '#011460'
                    genotype_1.variation_id = variation.id
                    genotype_1.source = 'http://www.ensembl.org/index.html'
                    genotype_1.save()

                    genotype_2 = VariationGenotype()
                    genotype_2.genotype = type_2
                    genotype_2.box_color = '#00B0F0'
                    genotype_2.source = 'http://www.ensembl.org/index.html'
                    genotype_2.variation_id = variation.id
                    genotype_2.save()

                    genotype_3 = VariationGenotype()
                    genotype_3.genotype = type_3
                    genotype_3.box_color = '#95C709'
                    genotype_3.source = 'http://www.ensembl.org/index.html'
                    genotype_3.variation_id = variation.id
                    genotype_3.save()

                    if 'effects' in variation_record:
                        self.generate_variation_block_effect(rsnumber, variation_record['effects'], variation, arr_allele)

                    if 'genename' in variation_record:
                        ## Add new association gene (genename)
                        variation_associated_variation = VariationAssociatedGene()
                        variation_associated_variation.gene_name = variation_record['genename']
                        variation_associated_variation.variation_id = variation.id
                        variation_associated_variation.save()

                    if 'associated_diseases' in variation_record:
                        ## Add new association disease
                        for disease in variation_record['associated_diseases']:
                            variation_associated_diseases_variation = VariationAssociatedDisease()
                            variation_associated_diseases_variation.disease_name = disease
                            variation_associated_diseases_variation.variation_id = variation.id
                            variation_associated_diseases_variation.save()

                    if 'associated_publications' in variation_record:
                        ## Add new association publication
                        for pub in variation_record['associated_publications']:
                            ## Create block fre
                            variation_associated_publications = VariationAssociatedPublication()
                            variation_associated_publications.title                   = pub['title']
                            variation_associated_publications.pmid                    = pub['pmid']
                            variation_associated_publications.variation_id            = variation.id
                            variation_associated_publications.save()

                    self.generate_variation_block_text_summary(rsnumber, variation_record, variation)
                    self.generate_variation_block_infobox(rsnumber, variation_record, variation)

                    if 'synonyms' in variation_record and variation_record['synonyms'] != None:
                        self.generate_variation_block_alias(rsnumber, variation_record['synonyms'], variation)

                    if '1000-genomes' in variation_record:
                        self.generate_variation_block_frequency(rsnumber, variation_record['1000-genomes'], variation)

                    if 'publications' in variation_record:
                        self.generate_variation_block_publication(rsnumber, variation_record['publications'], variation)

                    if "disgenet-diseases" in variation_record:
                        self.generate_variation_block_disgenet_diseases(rsnumber, variation_record['disgenet-diseases'], variation)
                        self.generate_variation_block_pub_text(rsnumber, variation_record['disgenet-diseases'], variation)


    def generate_variation_block_infobox(self,rsnumber, data, variation):
        ## Create block
        variation_block = VariationBlock()
        variation_block.kind = "variation_infobox"
        variation_block.position = "right"
        variation_block.sort_order = 5
        variation_block.title = 'Information '+ rsnumber
        variation_block.text = ''
        variation_block.variation_id = variation.id
        variation_block.save()

        ## Create fre version
        variation_block_infobox_version = VariationBlockInfoboxVersion()
        variation_block_infobox_version.author = 'anonymous'
        variation_block_infobox_version.version_status = 'active'
        variation_block_infobox_version.version = 1
        variation_block_infobox_version.is_stable = 1
        variation_block_infobox_version.variation_id = variation.id
        variation_block_infobox_version.variation_block_id = variation_block.id
        variation_block_infobox_version.save()

        ## Create default Infobox
        if 'chromosome' in data:
            variation_infobox = VariationBlockInfobox()
            variation_infobox.key                      = 'Chromosome'
            variation_infobox.value                    = data.get('chromosome', '')
            variation_infobox.variation_block_id = variation_block.id
            variation_infobox.variation_block_version_id = variation_block_infobox_version.id
            variation_infobox.save()

        if 'genename' in data:
            variation_infobox1 = VariationBlockInfobox()
            variation_infobox1.key                      = 'Gene name'
            variation_infobox1.value                    = data.get('genename', '')
            variation_infobox1.variation_block_id = variation_block.id
            variation_infobox1.variation_block_version_id = variation_block_infobox_version.id
            variation_infobox1.save()

    def generate_variation_block_publication(self, rsnumber, publications, variation):

        ## Create block
        variation_block = VariationBlock()
        variation_block.kind = "general_publications"
        variation_block.position = "left"
        variation_block.sort_order = 4
        variation_block.title = "Publication "+ rsnumber
        variation_block.text = ''
        variation_block.variation_id = variation.id
        variation_block.save()

        ## Create fre version
        variation_block_publications_version = VariationBlockPublicationVersion()
        variation_block_publications_version.author = "anonymous"
        variation_block_publications_version.version_status = 'active'
        variation_block_publications_version.version = 1
        variation_block_publications_version.is_stable = 1
        variation_block_publications_version.variation_id = variation.id
        variation_block_publications_version.variation_block_id = variation_block.id
        variation_block_publications_version.save()

        for pub in publications:
            ## Create block fre
            if pub.get('title', '') != '' and pub.get('pmid', '') != '' :
                variation_publications = VariationBlockPublication()
                variation_publications.title                   = pub['title']
                variation_publications.pmid                    = pub['pmid']
                variation_publications.doi                     = pub['doi']
                variation_publications.journal                 = pub.get('journal', '')
                variation_publications.authors                 = pub['authors']
                variation_publications.pmc                     = pub['pmcid']
                variation_publications.variation_block_id = variation_block.id
                variation_publications.variation_block_version_id = variation_block_publications_version.id
                variation_publications.save()

    def generate_variation_block_alias(self, rsnumber, alias, variation):

        ## Create block
        variation_block = VariationBlock()
        variation_block.kind = "general_alias"
        variation_block.position = "right"
        variation_block.sort_order = 4
        variation_block.title = "Other names for "+ rsnumber
        variation_block.text = ''
        variation_block.variation_id = variation.id
        variation_block.save()

        ## Create fre version
        variation_block_alias_version = VariationBlockAliasVersion()
        variation_block_alias_version.author = "anonymous"
        variation_block_alias_version.version_status = 'active'
        variation_block_alias_version.version = 1
        variation_block_alias_version.is_stable = 1
        variation_block_alias_version.variation_id = variation.id
        variation_block_alias_version.variation_block_id = variation_block.id
        variation_block_alias_version.save()

        for al in alias:
            ## Create block fre
            variation_alias = VariationBlockAlias()
            variation_alias.alias                   = al
            variation_alias.variation_block_id = variation_block.id
            variation_alias.variation_block_version_id = variation_block_alias_version.id
            variation_alias.save()

    def generate_variation_block_disgenet_diseases(self, rsnumber, disgenet_diseases, variation):

        ## Create block
        variation_block = VariationBlock()
        variation_block.kind = "general_disgenet_diseases"
        variation_block.position = "left"
        variation_block.sort_order = 4
        variation_block.title = rsnumber+ " is associated with the following Diseases"
        variation_block.text = ''
        variation_block.variation_id = variation.id
        variation_block.save()

        ## Create fre version
        variation_block_disgenet_diseases_version = VariationBlockDisgenetDiseasesVersion()
        variation_block_disgenet_diseases_version.author = "anonymous"
        variation_block_disgenet_diseases_version.version_status = 'active'
        variation_block_disgenet_diseases_version.version = 1
        variation_block_disgenet_diseases_version.is_stable = 1
        variation_block_disgenet_diseases_version.variation_id = variation.id
        variation_block_disgenet_diseases_version.variation_block_id = variation_block.id
        variation_block_disgenet_diseases_version.save()

        for val in disgenet_diseases:
            variation_disgenet_diseases = VariationBlockDisgenetDiseases()
            variation_disgenet_diseases.title                      = val['disease']
            variation_disgenet_diseases.pubmedid                   = val['pubmedid']
            variation_disgenet_diseases.variation_block_id         = variation_block.id
            variation_disgenet_diseases.variation_block_version_id = variation_block_disgenet_diseases_version.id
            variation_disgenet_diseases.save()

    def generate_variation_block_frequency(self,rsnumber, frequencies, variation):

        ## Create block
        variation_block = VariationBlock()
        variation_block.kind = "variation_frequency"
        variation_block.position = "right"
        variation_block.sort_order = 1
        variation_block.title = "How common is "+ rsnumber
        variation_block.text = ''
        variation_block.variation_id = variation.id
        variation_block.save()

        ## Create fre version
        variation_block_fre_version = VariationBlockFrequencyVersion()
        variation_block_fre_version.author = "anonymous"
        variation_block_fre_version.version_status = 'active'
        variation_block_fre_version.version = 1
        variation_block_fre_version.is_stable = 1
        variation_block_fre_version.variation_id = variation.id
        variation_block_fre_version.variation_block_id = variation_block.id
        variation_block_fre_version.save()

        for fre in frequencies:
            popcode = fre
            variation_fre = VariationBlockFrequency()
            variation_fre.popcode                   = popcode
            variation_fre.genotype_count_00         = frequencies[fre].get('00', 0)
            variation_fre.genotype_count_01         = frequencies[fre].get('01', 0)
            variation_fre.genotype_count_11         = frequencies[fre].get('11', 0)
            variation_fre.variation_block_id = variation_block.id
            variation_fre.variation_block_version_id = variation_block_fre_version.id
            variation_fre.save()

    def generate_variation_block_effect(self, rsnumber, effects, variation, alle_string):
        ## Create block
        variation_block = VariationBlock()
        variation_block.kind = "variation_effect"
        variation_block.position = "left"
        variation_block.sort_order = 3
        variation_block.title = "Effects "+ rsnumber
        variation_block.text = ''
        variation_block.variation_id = variation.id
        variation_block.save()

        ## Create effect version
        variation_block_eff_version = VariationBlockEffectVersion()
        variation_block_eff_version.author = "anonymous"
        variation_block_eff_version.version_status = 'active'
        variation_block_eff_version.version = 1
        variation_block_eff_version.is_stable = 1
        variation_block_eff_version.variation_id = variation.id
        variation_block_eff_version.variation_block_id = variation_block.id
        variation_block_eff_version.save()

        for eff in effects:
            ## Create block Effect
            if eff['risk_allele'] != '' and eff['risk_allele'] != '?':
                genotype = [alle_string[0]+"/"+alle_string[0], alle_string[1]+"/"+alle_string[1], alle_string[0]+"/"+alle_string[1],]
                ## Clone X/?
                variation_effect = VariationBlockEffect()
                odd_ratio = 0 if eff.get('odd_ratio', "") == "" else eff['odd_ratio']

                genotype_eff = alle_string[0]+"/"+ eff['risk_allele']
                if genotype_eff not in  genotype:
                    genotype_eff = eff['risk_allele'] + "/"+ alle_string[0]

                if alle_string[0] ==  eff['risk_allele']:
                    odd_ratio = float(odd_ratio)*float(odd_ratio)
                variation_effect.popcode        = eff.get('popcode', '')
                variation_effect.genotype       = genotype_eff
                variation_effect.risk           = eff['risk']
                variation_effect.odd_ratio      = odd_ratio
                variation_effect.evidences      = eff['evidences']
                variation_effect.pmid           = eff['pmid']
                variation_effect.variation_block_id = variation_block.id
                variation_effect.variation_block_version_id = variation_block_eff_version.id
                variation_effect.save()

                ## Clone X/X
                variation_effect_1 = VariationBlockEffect()
                odd_ratio = 0 if eff.get('odd_ratio', "") == "" else eff['odd_ratio']

                genotype_eff = alle_string[1]+"/"+ eff['risk_allele']
                if genotype_eff not in genotype:
                    genotype_eff = eff['risk_allele'] + "/"+ alle_string[1]

                if alle_string[1] ==  eff['risk_allele']:
                    odd_ratio = float(odd_ratio)*float(odd_ratio)
                variation_effect_1.popcode        = eff.get('popcode', '')
                variation_effect_1.genotype       = genotype_eff
                variation_effect_1.risk           = eff['risk']
                variation_effect_1.odd_ratio      = odd_ratio
                variation_effect_1.evidences      = eff['evidences']
                variation_effect_1.pmid           = eff['pmid']
                variation_effect_1.variation_block_id = variation_block.id
                variation_effect_1.variation_block_version_id = variation_block_eff_version.id
                variation_effect_1.save()



    def generate_variation_block_text_summary(self, rsnumber, dataVariation, variation):
        genename = ""
        if 'genename' in dataVariation:
            genename = dataVariation['genename']
        text = 'If you compare the DNA strand from different people, the genetic code letters will be virtually identical. On average, only about one in 1000 genetic letters (called bases) will differ from one person to the next. These positions, where some people have one letter and other people have another are called SNPs.'
        text += rsnumber+ ' is a SNP, that sits on a specific position on 1, right where the '+ genename +' gene is located. Most people have the genetic letter "2" at this position, but at least some individuals have the letter "1" in this position instead.'

        ## Create block text summary
        variation_block = VariationBlock()
        variation_block.kind = "general_text"
        variation_block.position = "left"
        variation_block.title = rsnumber+ " summary"
        variation_block.text = ''
        variation_block.sort_order = 5
        variation_block.variation_id = variation.id
        variation_block.save()

        ## Block text version
        variation_block_version = VariationBlockVersion()
        variation_block_version.variation_block_id = variation_block.id
        variation_block_version.variation_id = variation.id
        variation_block_version.title = rsnumber+ ' is a genetic variation, also called "SNP"'
        variation_block_version.text = text
        # Set status active
        variation_block_version.version_status = 'active'
        variation_block_version.is_stable = True
        variation_block_version.author = 'anonymous' # Fix me
        # Set version
        variation_block_version.version = 1
        variation_block_version.save()

    def generate_variation_block_pub_text(self, rsnumber, dataVariation, variation):

        ## Create block
        variation_block = VariationBlock()
        variation_block.kind = "variation_pub_text"
        variation_block.position = "left"
        variation_block.sort_order = 3
        variation_block.title = "Relevant Extracts from Publications"
        variation_block.text = ''
        variation_block.variation_id = variation.id
        variation_block.save()
        ## Group data by PMIDID
        arr_data = {}
        for val in dataVariation:
            if val['pubmedid'] in arr_data:
                if arr_data[val['pubmedid']]['disease'] != val['disease'].strip():
                    arr_data[val['pubmedid']]['sentence'] += val.get('sentence', '')+ "\n"
            else:
                arr_data[val['pubmedid']] = {
                    'disease':      val['disease'].strip(" "),
                    'pubmedid':     val['pubmedid'],
                    'sentence':     val['sentence']
                }
        ## Create effect version
        variation_block_pub_text_version = VariationBlockPublicationTextVersion()
        variation_block_pub_text_version.author = "anonymous"
        variation_block_pub_text_version.version_status = 'active'
        variation_block_pub_text_version.version = 1
        variation_block_pub_text_version.is_stable = 1
        variation_block_pub_text_version.variation_id = variation.id
        variation_block_pub_text_version.variation_block_id = variation_block.id
        variation_block_pub_text_version.save()

        ## Create block
        for val in arr_data:
            variation_pub_text = VariationBlockPublicationText()
            variation_pub_text.title           = ''
            variation_pub_text.pubmedid        = arr_data[val]['pubmedid']
            variation_pub_text.sentence        = arr_data[val]['sentence']
            variation_pub_text.variation_block_id = variation_block.id
            variation_pub_text.variation_block_version_id = variation_block_pub_text_version.id
            variation_pub_text.save()
