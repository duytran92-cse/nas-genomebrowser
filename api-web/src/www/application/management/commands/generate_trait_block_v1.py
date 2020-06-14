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
            self.generate_trait(data)

            print "="*10+ "=> Generate trait " + data['name'] + " => Done"
        print "[*] To exit press CTRL+C"

    def consume(self, ch, method, properties, body):
        record = json.loads(body)
        data = []
        data = record
        data.update(record['core_attributes'])
        data.pop('core_attributes')
        self.generate_trait(data)

        print "="*10+ "=> Generate trait " + data['name'] + " => Done"
        print "[*] To exit press CTRL+C"

    def handle(self, *args, **kwargs):
        print "[x] RECEIVING DATA"

        credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASS)
        connection = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBITMQ_HOST, settings.RABBITMQ_PORT, '/', credentials))

        channel = connection.channel()
        # channel.queue_declare(queue=settings.GENODATA_QUEUE_TRAIT, durable=True) ## <=== Local
        channel.queue_declare(queue=settings.GENODATA_QUEUE_TRAIT)

        print "[*] Waiting for data. To exit press CTRL+C"


        # channel.basic_consume(self.consume_local, queue=settings.GENODATA_QUEUE_TRAIT, no_ack=True) ## <=== Local
        channel.basic_consume(self.consume, queue=settings.GENODATA_QUEUE_TRAIT, no_ack=True)
        channel.start_consuming()

    ## ====================================================================
    ## Trait
    def generate_trait(self, trait_record):
        trait_name = trait_record['name']
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
