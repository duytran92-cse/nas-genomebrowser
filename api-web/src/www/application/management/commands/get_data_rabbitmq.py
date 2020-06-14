import json, pika, os
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from notasquare.urad_api.containers.standard import Container
from application.models import *
from django.conf import settings

class Command(BaseCommand):
    def consume(self, ch, method, properties, body):
        print body

    def handle(self, *args, **kwargs):

        credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASS)
        connection = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBITMQ_HOST, settings.RABBITMQ_PORT, '/', credentials))

        channel = connection.channel()
        # channel.queue_declare(queue=settings.GENODATA_QUEUE, durable=True) ## <=== Local

        channel.queue_declare(queue=settings.GENODATA_QUEUE_VARIATION)

        channel.basic_consume(self.consume, queue=settings.GENODATA_QUEUE_VARIATION, no_ack=True)
        channel.start_consuming()
