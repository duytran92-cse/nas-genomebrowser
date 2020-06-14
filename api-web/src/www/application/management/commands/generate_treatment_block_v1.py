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
            self.generate_treatment(data)

            print "="*10+ "=> Generate treatment " + data['name'] + " => Done"
        print "[*] To exit press CTRL+C"

    def consume(self, ch, method, properties, body):
        record = json.loads(body)
        data = []
        data = record
        data.update(record['core_attributes'])
        data.pop('core_attributes')
        self.generate_treatment(data)

        print "="*10+ "=> Generate treatment " + data['name'] + " => Done"
        print "[*] To exit press CTRL+C"

    def handle(self, *args, **kwargs):
        print "[x] RECEIVING DATA"

        credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASS)
        connection = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBITMQ_HOST, settings.RABBITMQ_PORT, '/', credentials))

        channel = connection.channel()
        # channel.queue_declare(queue=settings.GENODATA_QUEUE_TREATMENT, durable=True) ## <=== Local
        channel.queue_declare(queue=settings.GENODATA_QUEUE_TREATMENT)

        print "[*] Waiting for data. To exit press CTRL+C"


        # channel.basic_consume(self.consume_local, queue=settings.GENODATA_QUEUE_TREATMENT, no_ack=True) ## <=== Local
        channel.basic_consume(self.consume, queue=settings.GENODATA_QUEUE_TREATMENT, no_ack=True)
        channel.start_consuming()

    ## ====================================================================
    ## Treatment
    def generate_treatment(self, treatment_record):
        treatment_name = treatment_record['name']
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
