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
            data = record[2]

            data.update({
                'entity':             record[0],
                record[0]:            record[1],
            })
            if data['entity'] == 'disease':
                self.generate_disease(data)
                print "="*10+ "=> Generate disease " + data['disease'] + " => Done"

            if data['entity'] == 'treatment':
                self.generate_treatment(data)
                print "="*10+ "=> Generate treatment " + data['treatment'] + " => Done"

            if data['entity'] == 'trait':
                self.generate_trait(data)
                print "="*10+ "=> Generate trait " + data['trait'] + " => Done"

            if data['entity'] == 'gene':
                self.generate_gene(data)
                print "="*10+ "=> Generate gene " + data['gene'] + " => Done"

            if data['entity'] == 'variation':
                self.generate_variation(data)
                print "="*10+ "=> Generate variation " + data['variation'] + " => Done"
        print "[*] To exit press CTRL+C"

    def consume(self, ch, method, properties, body):
        record = json.loads(body)
        data = []
        data = record[2]
        data.update({
            'entity':             record[0],
            record[0]:            record[1],
        })
        if data['entity'] == 'disease':
            self.generate_disease(data)
            print "="*10+ "=> Generate disease " + data['disease'] + " => Done"

        if data['entity'] == 'treatment':
            self.generate_treatment(data)
            print "="*10+ "=> Generate treatment " + data['treatment'] + " => Done"

        if data['entity'] == 'trait':
            self.generate_trait(data)
            print "="*10+ "=> Generate trait " + data['trait'] + " => Done"

        if data['entity'] == 'gene':
            self.generate_gene(data)
            print "="*10+ "=> Generate gene " + data['gene'] + " => Done"

        if data['entity'] == 'variation':
            self.generate_variation(data)
            print "="*10+ "=> Generate variation " + data['variation'] + " => Done"
        print "[*] To exit press CTRL+C"

    def handle(self, *args, **kwargs):
        print "[x] RECEIVING DATA"

        credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASS)
        connection = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBITMQ_HOST, settings.RABBITMQ_PORT, '/', credentials))

        channel = connection.channel()
        # channel.queue_declare(queue=settings.GENODATA_QUEUE, durable=True) ## <=== Local
        channel.queue_declare(queue=settings.GENODATA_QUEUE)

        print "[*] Waiting for data. To exit press CTRL+C"


        # channel.basic_consume(self.consume_local, queue=settings.GENODATA_QUEUE, no_ack=True) ## <=== Local
        channel.basic_consume(self.consume, queue=settings.GENODATA_QUEUE, no_ack=True)
        channel.start_consuming()

    ## ====================================================================
    ## Disease
    def generate_disease(self, disease_record):
        disease_name = disease_record['disease']
        query = Disease.objects.filter(title = disease_name)

        if query.count() == 0:
            disease = Disease()
            disease.title = disease_name
            disease.save()
            self.generate_disease_block_text_summary(disease_name, disease_record, disease)

            if 'associated_gene' in disease_record:
                ## Add new association gene
                for ass_disease in disease_record['associated_gene']:
                    disease_associated_disease = DiseaseAssociatedGene()
                    disease_associated_disease.gene_name = ass_disease
                    disease_associated_disease.disease_id = disease.id
                    disease_associated_disease.save()

            if 'associated_publications' in disease_record:
                ## Add new association publication
                for pub in disease_record['associated_publications']:
                    ## Create block fre
                    disease_associated_publications = DiseaseAssociatedPublication()
                    disease_associated_publications.title                   = pub['title']
                    disease_associated_publications.pmid                    = pub['pmid']
                    disease_associated_publications.doi                     = pub['doi']
                    disease_associated_publications.journal                 = pub['journal']
                    disease_associated_publications.authors                 = pub['authors']
                    disease_associated_publications.pmc                     = pub['pmc']
                    disease_associated_publications.disease_id              = disease.id
                    disease_associated_publications.save()

            if 'synonyms' in disease_record:
                self.generate_disease_block_alias(disease_name, disease_record['synonyms'], disease)

            if 'publications' in disease_record:
                self.generate_disease_block_publication(disease_name, disease_record['publications'], disease)

    def generate_disease_block_publication(self,disease_name, publications, disease):

        ## Create block
        disease_block = DiseaseBlock()
        disease_block.kind = "general_publications"
        disease_block.position = "left"
        disease_block.sort_order = 1
        disease_block.title = "Publications "+ disease_name
        disease_block.text = ''
        disease_block.disease_id = disease.id
        disease_block.save()

        ## Create fre version
        disease_block_publications_version = DiseaseBlockPublicationVersion()
        disease_block_publications_version.author = 'anonymous'
        disease_block_publications_version.version_status = 'active'
        disease_block_publications_version.version = 1
        disease_block_publications_version.is_stable = 1
        disease_block_publications_version.disease_id = disease.id
        disease_block_publications_version.disease_block_id = disease_block.id
        disease_block_publications_version.save()

        for pub in publications:
            ## Create block fre
            disease_publications = DiseaseBlockPublication()
            disease_publications.title                   = pub['title']
            disease_publications.pmid                    = pub['pmid']
            disease_publications.doi                     = pub['doi']
            disease_publications.journal                 = pub['journal']
            disease_publications.authors                 = pub['authors']
            disease_publications.pmc                     = pub['pmc']
            disease_publications.disease_block_id = disease_block.id
            disease_publications.disease_block_version_id = disease_block_publications_version.id
            disease_publications.save()

    def generate_disease_block_alias(self, disease_name, alias, disease):

        ## Create block
        disease_block = DiseaseBlock()
        disease_block.kind = "general_alias"
        disease_block.position = "right"
        disease_block.sort_order = 1
        disease_block.title = "Alias"
        disease_block.text = ''
        disease_block.disease_id = disease.id
        disease_block.save()

        ## Create fre version
        disease_block_alias_version = DiseaseBlockAliasVersion()
        disease_block_alias_version.author = "anonymous"
        disease_block_alias_version.version_status = 'active'
        disease_block_alias_version.version = 1
        disease_block_alias_version.is_stable = 1
        disease_block_alias_version.disease_id = disease.id
        disease_block_alias_version.disease_block_id = disease_block.id
        disease_block_alias_version.save()

        for al in alias:
            ## Create block fre
            disease_alias = DiseaseBlockAlias()
            disease_alias.alias                   = al
            disease_alias.disease_block_id = disease_block.id
            disease_alias.disease_block_version_id = disease_block_alias_version.id
            disease_alias.save()

    def generate_disease_block_text_summary(self, disease_name, dataDisease, disease):

        text = ''
        ## Create block text summary
        disease_block = DiseaseBlock()
        disease_block.kind = "general_text"
        disease_block.position = "main"
        disease_block.title = disease_name+ " summary"
        disease_block.text = ''
        disease_block.sort_order = 1
        disease_block.disease_id = disease.id
        disease_block.save()

        ## Block text version
        disease_block_version = DiseaseBlockVersion()
        disease_block_version.disease_block_id = disease_block.id
        disease_block_version.disease_id = disease.id
        disease_block_version.title = "How common is "+ disease_name
        disease_block_version.text = text
        # Set status active
        disease_block_version.version_status = 'active'
        disease_block_version.is_stable = True
        disease_block_version.author = 'anonymous' # Fix me
        # Set version
        disease_block_version.version = 1
        disease_block_version.save()

    ## ====================================================================
    ## Gene
    def generate_gene(self, gene_record):
        gene_name = gene_record['gene']
        query = Gene.objects.filter(title = gene_name)
        if query.count() == 0:
            if gene_record.get('start', 0) != 0 and gene_record.get('end', 0) != 0:
                gene = Gene()
                gene.title = gene_record['gene']
                gene.save()

                if 'associated_diseases' in gene_record:
                    ## Add new association disease
                    for ass_disease in gene_record['associated_diseases']:
                        gene_associated_disease = GeneAssociatedDisease()
                        gene_associated_disease.disease_name = ass_disease
                        gene_associated_disease.gene_id = gene.id
                        gene_associated_disease.save()


                if 'associated_publications' in gene_record:
                ## Add new association publication
                    for pub in gene_record['associated_publications']:
                        ## Create block fre
                        gene_associated_publications = GeneAssociatedPublication()
                        gene_associated_publications.title                   = pub['title']
                        gene_associated_publications.pmid                    = pub['pmid']
                        gene_associated_publications.gene_id                 = gene.id
                        gene_associated_publications.save()

                self.generate_gene_block_text_summary(gene_name, gene_record, gene)
                self.generate_gene_block_infobox(gene_name, gene_record, gene)

                if 'synonyms' in gene_record:
                    self.generate_gene_block_alias(gene_name, gene_record['synonyms'], gene)

                if 'effects' in gene_record:
                    self.generate_gene_block_effect(gene_name, gene_record['effects'], gene)

                if 'publications' in gene_record:
                    self.generate_gene_block_publication(gene_name, gene_record['publications'], gene)

    def generate_gene_block_infobox(self,gene_name, data, gene):

        ## Create block
        gene_block = GeneBlock()
        gene_block.kind = "gene_infobox"
        gene_block.position = "left"
        gene_block.sort_order = 1
        gene_block.title = 'Information '+ gene_name
        gene_block.text = ''
        gene_block.gene_id = gene.id
        gene_block.save()

        ## Create fre version
        gene_block_infobox_version = GeneBlockInfoboxVersion()
        gene_block_infobox_version.author = 'anonymous'
        gene_block_infobox_version.version_status = 'active'
        gene_block_infobox_version.version = 1
        gene_block_infobox_version.is_stable = 1
        gene_block_infobox_version.gene_id = gene.id
        gene_block_infobox_version.gene_block_id = gene_block.id
        gene_block_infobox_version.save()

        ## Create default Infobox
        gene_infobox = GeneBlockInfobox()
        gene_infobox.description              = data.get('description', '')
        gene_infobox.chromosome               = data.get('chromosome', '')
        gene_infobox.start                    = data.get('start', '0')
        gene_infobox.end                      = data.get('end', '0')
        gene_infobox.number_of_exons          = data.get('num_exon', '0')
        gene_infobox.protein_products         = data.get('protein_product', '') ## <== check
        gene_infobox.gene_block_id = gene_block.id
        gene_infobox.gene_block_version_id = gene_block_infobox_version.id
        gene_infobox.save()

    def generate_gene_block_publication(self,gene_name, publications, gene):

        ## Create block
        gene_block = GeneBlock()
        gene_block.kind = "general_publications"
        gene_block.position = "right"
        gene_block.sort_order = 1
        gene_block.title = "Publication "+ gene_name
        gene_block.text = ''
        gene_block.gene_id = gene.id
        gene_block.save()

        ## Create fre version
        gene_block_publications_version = GeneBlockPublicationVersion()
        gene_block_publications_version.author = "anonymous"
        gene_block_publications_version.version_status = 'active'
        gene_block_publications_version.version = 1
        gene_block_publications_version.is_stable = 1
        gene_block_publications_version.gene_id = gene.id
        gene_block_publications_version.gene_block_id = gene_block.id
        gene_block_publications_version.save()

        for pub in publications:
            ## Create block fre
            gene_publications = GeneBlockPublication()
            gene_publications.title                   = pub['title']
            gene_publications.pmid                    = pub['pmid']
            gene_publications.doi                     = pub['doi']
            gene_publications.journal                 = pub['journal']
            gene_publications.authors                 = pub['authors']
            gene_publications.pmc                     = pub['pmc']
            gene_publications.gene_block_id = gene_block.id
            gene_publications.gene_block_version_id = gene_block_publications_version.id
            gene_publications.save()

    def generate_gene_block_alias(self, gene_name, alias, gene):

        ## Create block
        gene_block = GeneBlock()
        gene_block.kind = "general_alias"
        gene_block.position = "left"
        gene_block.sort_order = 1
        gene_block.title = "Alias"
        gene_block.text = ''
        gene_block.gene_id = gene.id
        gene_block.save()

        ## Create fre version
        gene_block_alias_version = GeneBlockAliasVersion()
        gene_block_alias_version.author = "anonymous"
        gene_block_alias_version.version_status = 'active'
        gene_block_alias_version.version = 1
        gene_block_alias_version.is_stable = 1
        gene_block_alias_version.gene_id = gene.id
        gene_block_alias_version.gene_block_id = gene_block.id
        gene_block_alias_version.save()

        for al in alias:
            ## Create block fre
            gene_alias = GeneBlockAlias()
            gene_alias.alias                   = al
            gene_alias.gene_block_id = gene_block.id
            gene_alias.gene_block_version_id = gene_block_alias_version.id
            gene_alias.save()

    def generate_gene_block_effect(self,gene_name, data_effect, gene):

        ## Create block
        gene_block = GeneBlock()
        gene_block.kind = "gene_effect"
        gene_block.position = "left"
        gene_block.sort_order = 1
        gene_block.title = "Effects "+ gene_name
        gene_block.text = ''
        gene_block.gene_id = gene.id
        gene_block.save()

        ## Create effect version
        gene_block_eff_version = GeneBlockEffectVersion()
        gene_block_eff_version.author = "anonymous"
        gene_block_eff_version.version_status = 'active'
        gene_block_eff_version.version = 1
        gene_block_eff_version.is_stable = 1
        gene_block_eff_version.gene_id = gene.id
        gene_block_eff_version.gene_block_id = gene_block.id
        gene_block_eff_version.save()

        ## Create block Effect
        for eff in data_effect:
            gene_effect = GeneBlockEffect()
            gene_effect.type           = eff['type']
            gene_effect.evidence       = eff['evidence']
            gene_effect.publication    = eff['publication']
            gene_effect.effect         = eff['effect']
            gene_effect.gene_block_id = gene_block.id
            gene_effect.gene_block_version_id = gene_block_eff_version.id
            gene_effect.save()

    def generate_gene_block_text_summary(self, gene_name, dataGene, gene):

        text = 'The '+ gene_name + " gene provides instructions for making an enzyme called. This enzyme plays a role in processing amino acids, the building blocks of proteins."
        text += ' It is part of the renin-angiotensin system, which regulates blood pressure and the balance of fluids and salts in the body. By cutting a protein called angiotensin I at a particular location, the angiotensin-converting enzyme converts this protein to angiotensin II. Angiotensin II causes blood vessels to narrow (constrict), which results in increased blood pressure. This protein also stimulates production of the hormone aldosterone, which triggers the absorption of salt and water by the kidneys. The increased amount of fluid in the body also increases blood pressure. Proper blood pressure during fetal growth, which delivers oxygen to the developing tissues, is required for normal development of the kidneys, particularly of structures called the proximal tubules, and other tissues. In addition, angiotensin II may play a more direct role in kidney development, perhaps by affecting growth factors involved in the development of kidney structures.'
        text += ' The angiotensin-converting enzyme can cleave other proteins, including bradykinin. Bradykinin causes blood vessels to widen (dilate), which decreases blood pressure. Cleavage by the angiotensin-converting enzyme inactivates bradykinin, helping to increase blood pressure.'

        ## Create block text summary
        gene_block = GeneBlock()
        gene_block.kind = "general_text"
        gene_block.position = "right"
        gene_block.title = gene_name+ " summary"
        gene_block.text = text
        gene_block.sort_order = 1
        gene_block.gene_id = gene.id
        gene_block.save()

        ## Block text version
        gene_block_version = GeneBlockVersion()
        gene_block_version.gene_block_id = gene_block.id
        gene_block_version.gene_id = gene.id
        gene_block_version.title = 'What is the function of the '+ gene_name +" gene?"
        gene_block_version.text = text
        # Set status active
        gene_block_version.version_status = 'active'
        gene_block_version.is_stable = True
        gene_block_version.author = 'anonymous' # Fix me
        # Set version
        gene_block_version.version = 1
        gene_block_version.save()

    ## ====================================================================
    ## Trait
    def generate_trait(self, trait_record):
        trait_name = trait_record['trait']
        query = Trait.objects.filter(title = trait_name)
        if query.count() == 0:
            trait = Trait()
            trait.title = trait_name
            trait.save()
            self.generate_trait_block_text_summary(trait_name, trait_record, trait)
            if 'synonyms' in trait_record:
                self.generate_trait_block_alias(trait_name, trait_record['synonyms'], trait)

            if 'publications' in trait_record:
                self.generate_trait_block_publication(trait_name, trait_record['publications'], trait)

    def generate_trait_block_publication(self,trait_name, publications, trait):

        ## Create block
        trait_block = TraitBlock()
        trait_block.kind = "general_publications"
        trait_block.position = "left"
        trait_block.sort_order = 1
        trait_block.title = "Publications "+ trait_name
        trait_block.text = ''
        trait_block.trait_id = trait.id
        trait_block.save()

        ## Create fre version
        trait_block_publications_version = TraitBlockPublicationVersion()
        trait_block_publications_version.author = 'anonymous'
        trait_block_publications_version.version_status = 'active'
        trait_block_publications_version.version = 1
        trait_block_publications_version.is_stable = 1
        trait_block_publications_version.trait_id = trait.id
        trait_block_publications_version.trait_block_id = trait_block.id
        trait_block_publications_version.save()

        for pub in publications:
            ## Create block fre
            trait_publications = TraitBlockPublication()
            trait_publications.title                   = pub['title']
            trait_publications.pmid                    = pub['pmid']
            trait_publications.doi                     = pub['doi']
            trait_publications.journal                 = pub['journal']
            trait_publications.authors                 = pub['authors']
            trait_publications.pmc                     = pub['pmc']
            trait_publications.trait_block_id = trait_block.id
            trait_publications.trait_block_version_id = trait_block_publications_version.id
            trait_publications.save()

    def generate_trait_block_alias(self, trait_name, alias, trait):

        ## Create block
        trait_block = TraitBlock()
        trait_block.kind = "general_alias"
        trait_block.position = "right"
        trait_block.sort_order = 1
        trait_block.title = "Alias"
        trait_block.text = ''
        trait_block.trait_id = trait.id
        trait_block.save()

        ## Create fre version
        trait_block_alias_version = TraitBlockAliasVersion()
        trait_block_alias_version.author = "anonymous"
        trait_block_alias_version.version_status = 'active'
        trait_block_alias_version.version = 1
        trait_block_alias_version.is_stable = 1
        trait_block_alias_version.trait_id = trait.id
        trait_block_alias_version.trait_block_id = trait_block.id
        trait_block_alias_version.save()

        for al in alias:
            ## Create block fre
            trait_alias = TraitBlockAlias()
            trait_alias.alias                   = al
            trait_alias.trait_block_id = trait_block.id
            trait_alias.trait_block_version_id = trait_block_alias_version.id
            trait_alias.save()

    def generate_trait_block_text_summary(self, trait_name, dataTrait, trait):

        text = ''
        ## Create block text summary
        trait_block = TraitBlock()
        trait_block.kind = "general_text"
        trait_block.position = "main"
        trait_block.title = trait_name+ " summary"
        trait_block.text = ''
        trait_block.sort_order = 1
        trait_block.trait_id = trait.id
        trait_block.save()

        ## Block text version
        trait_block_version = TraitBlockVersion()
        trait_block_version.trait_block_id = trait_block.id
        trait_block_version.trait_id = trait.id
        trait_block_version.title = "How common is "+ trait_name
        trait_block_version.text = text
        # Set status active
        trait_block_version.version_status = 'active'
        trait_block_version.is_stable = True
        trait_block_version.author = 'anonymous' # Fix me
        # Set version
        trait_block_version.version = 1
        trait_block_version.save()

    ## ====================================================================
    ## Treatment
    def generate_treatment(self, treatment_record):
        treatment_name = treatment_record['treatment']
        query = Treatment.objects.filter(title = treatment_name)
        if query.count() == 0:
            treatment = Treatment()
            treatment.title = treatment_name
            treatment.save()

            self.generate_treatment_block_text_summary(treatment_name, treatment_record, treatment)
            if 'synonyms' in treatment_record:
                self.generate_treatment_block_alias(treatment_name, treatment_record['synonyms'], treatment)

            if 'publications' in treatment_record:
                self.generate_treatment_block_publication(treatment_name, treatment_record['publications'], treatment)

    def generate_treatment_block_publication(self,treatment_name, publications, treatment):

        ## Create block
        treatment_block = TreatmentBlock()
        treatment_block.kind = "general_publications"
        treatment_block.position = "left"
        treatment_block.sort_order = 1
        treatment_block.title = "Publications "+ treatment_name
        treatment_block.text = ''
        treatment_block.treatment_id = treatment.id
        treatment_block.save()

        ## Create fre version
        treatment_block_publications_version = TreatmentBlockPublicationVersion()
        treatment_block_publications_version.author = 'anonymous'
        treatment_block_publications_version.version_status = 'active'
        treatment_block_publications_version.version = 1
        treatment_block_publications_version.is_stable = 1
        treatment_block_publications_version.treatment_id = treatment.id
        treatment_block_publications_version.treatment_block_id = treatment_block.id
        treatment_block_publications_version.save()

        for pub in publications:
            ## Create block fre
            treatment_publications = TreatmentBlockPublication()
            treatment_publications.title                   = pub['title']
            treatment_publications.pmid                    = pub['pmid']
            treatment_publications.doi                     = pub['doi']
            treatment_publications.journal                 = pub['journal']
            treatment_publications.authors                 = pub['authors']
            treatment_publications.pmc                     = pub['pmc']
            treatment_publications.treatment_block_id = treatment_block.id
            treatment_publications.treatment_block_version_id = treatment_block_publications_version.id
            treatment_publications.save()

    def generate_treatment_block_alias(self, treatment_name, alias, treatment):

        ## Create block
        treatment_block = TreatmentBlock()
        treatment_block.kind = "general_alias"
        treatment_block.position = "right"
        treatment_block.sort_order = 1
        treatment_block.title = "Alias"
        treatment_block.text = ''
        treatment_block.treatment_id = treatment.id
        treatment_block.save()

        ## Create fre version
        treatment_block_alias_version = TreatmentBlockAliasVersion()
        treatment_block_alias_version.author = "anonymous"
        treatment_block_alias_version.version_status = 'active'
        treatment_block_alias_version.version = 1
        treatment_block_alias_version.is_stable = 1
        treatment_block_alias_version.treatment_id = treatment.id
        treatment_block_alias_version.treatment_block_id = treatment_block.id
        treatment_block_alias_version.save()

        for al in alias:
            ## Create block fre
            treatment_alias = TreatmentBlockAlias()
            treatment_alias.alias                   = al
            treatment_alias.treatment_block_id = treatment_block.id
            treatment_alias.treatment_block_version_id = treatment_block_alias_version.id
            treatment_alias.save()

    def generate_treatment_block_text_summary(self, treatment_name, dataTreatment, treatment):

        text = ''
        ## Create block text summary
        treatment_block = TreatmentBlock()
        treatment_block.kind = "general_text"
        treatment_block.position = "main"
        treatment_block.title = treatment_name+ " summary"
        treatment_block.text = ''
        treatment_block.sort_order = 1
        treatment_block.treatment_id = treatment.id
        treatment_block.save()

        ## Block text version
        treatment_block_version = TreatmentBlockVersion()
        treatment_block_version.treatment_block_id = treatment_block.id
        treatment_block_version.treatment_id = treatment.id
        treatment_block_version.title = "How common is "+ treatment_name
        treatment_block_version.text = text
        # Set status active
        treatment_block_version.version_status = 'active'
        treatment_block_version.is_stable = True
        treatment_block_version.author = 'anonymous' # Fix me
        # Set version
        treatment_block_version.version = 1
        treatment_block_version.save()

    ## ====================================================================
    ## Variation
    def generate_variation(self, variation_record):
        if variation_record.get('allele_string', '') != '':
            arr_allele = variation_record['allele_string'].split('/')
            if len(arr_allele) == 2:
                rsnumber = variation_record['variation']
                query = Variation.objects.filter(title = rsnumber)
                if query.count() == 0:
                    variation = Variation()
                    variation.title = rsnumber
                    variation.save()

                    ## Add new Genotype ##

                    type_1 = arr_allele[0]+ "/"+ arr_allele[0]
                    type_2 = arr_allele[0]+ "/"+ arr_allele[1]
                    type_3 = arr_allele[1]+ "/"+ arr_allele[1]
                    genotype_1 = VariationBlockGenotype()
                    genotype_1.genotype = type_1
                    genotype_1.box_color = '#011460'
                    genotype_1.variation_id = variation.id
                    genotype_1.save()

                    genotype_2 = VariationBlockGenotype()
                    genotype_2.genotype = type_2
                    genotype_2.box_color = '#00B0F0'
                    genotype_2.variation_id = variation.id
                    genotype_2.save()

                    genotype_3 = VariationBlockGenotype()
                    genotype_3.genotype = type_3
                    genotype_3.box_color = '#95C709'
                    genotype_3.variation_id = variation.id
                    genotype_3.save()

                    if 'gwas-effects' in variation_record:
                        self.generate_variation_block_effect(rsnumber, variation_record['gwas-effects'], variation, arr_allele)

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

                    if 'synonyms' in variation_record:
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
                variation_effect.risk           = eff['risk_allele']
                variation_effect.odd_ratio      = odd_ratio
                variation_effect.evidences       = eff['initial']        ##eff['evidences']
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
                variation_effect_1.risk           = eff['risk_allele']
                variation_effect_1.odd_ratio      = odd_ratio
                variation_effect_1.evidences      = eff['initial']        ##eff['evidences']
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
