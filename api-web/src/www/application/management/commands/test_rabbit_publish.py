import json, pika, os
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from notasquare.urad_api.containers.standard import Container
from application.models import *
from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print "Publish data to rabbitmq"
        data = []
        with open("gene.txt") as f:
            for line in f:
                data.append(json.loads(line))

        credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASS)
        connection = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBITMQ_HOST, settings.RABBITMQ_PORT, '/', credentials))

        channel = connection.channel()

        channel.queue_declare(queue='genome-browser-gene', durable=True)
        message = json.dumps(data)
        channel.basic_publish(exchange='',
                              routing_key='genome-browser-gene',
                              body=message)
        print(" [x] Sent data to RabbitMQ")
        connection.close()
