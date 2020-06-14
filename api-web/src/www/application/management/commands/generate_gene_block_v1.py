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
            self.generate_gene(data)

            print "="*10+ "=> Generate gene " + data['name'] + " => Done"
        print "[*] To exit press CTRL+C"

    def consume(self, ch, method, properties, body):
        record = json.loads(body)
        data = []
        data = record
        data.update(record['core_attributes'])
        data.pop('core_attributes')
        self.generate_gene(data)

        print "="*10+ "=> Generate gene " + data['name'] + " => Done"
        print "[*] To exit press CTRL+C"

    def handle(self, *args, **kwargs):
        print "[x] RECEIVING DATA"

        credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASS)
        connection = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBITMQ_HOST, settings.RABBITMQ_PORT, '/', credentials))

        channel = connection.channel()
        # channel.queue_declare(queue=settings.GENODATA_QUEUE_GENE, durable=True) ## <=== Local
        channel.queue_declare(queue=settings.GENODATA_QUEUE_GENE)

        print "[*] Waiting for data. To exit press CTRL+C"


        # channel.basic_consume(self.consume_local, queue=settings.GENODATA_QUEUE_GENE, no_ack=True) ## <=== Local
        channel.basic_consume(self.consume, queue=settings.GENODATA_QUEUE_GENE, no_ack=True)
        channel.start_consuming()

    ## ====================================================================
    ## Gene
    def generate_gene(self, gene_record):
        gene_name = gene_record['name']
        query = Gene.objects.filter(title = gene_name)
        if query.count() == 0:
            if gene_record.get('start', 0) != 0 and gene_record.get('end', 0) != 0:
                gene = Gene()
                gene.title = gene_record['name']
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
