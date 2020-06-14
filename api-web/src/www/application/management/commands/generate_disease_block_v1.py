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
            self.generate_disease(data)

            print "="*10+ "=> Generate disease " + data['name'] + " => Done"
        print "[*] To exit press CTRL+C"

    def consume(self, ch, method, properties, body):
        record = json.loads(body)
        data = []
        data = record
        data.update(record['core_attributes'])
        data.pop('core_attributes')
        self.generate_disease(data)

        print "="*10+ "=> Generate disease " + data['name'] + " => Done"
        print "[*] To exit press CTRL+C"

    def handle(self, *args, **kwargs):
        print "[x] RECEIVING DATA"

        credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASS)
        connection = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBITMQ_HOST, settings.RABBITMQ_PORT, '/', credentials))

        channel = connection.channel()
        # channel.queue_declare(queue=settings.GENODATA_QUEUE_DISEASE, durable=True) ## <=== Local
        channel.queue_declare(queue=settings.GENODATA_QUEUE_DISEASE)

        print "[*] Waiting for data. To exit press CTRL+C"


        # channel.basic_consume(self.consume_local, queue=settings.GENODATA_QUEUE_DISEASE, no_ack=True) ## <=== Local
        channel.basic_consume(self.consume, queue=settings.GENODATA_QUEUE_DISEASE, no_ack=True)
        channel.start_consuming()

    ## ====================================================================
    ## Disease
    def generate_disease(self, disease_record):
        disease_name = disease_record['name']
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
