import json, pika, os
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from notasquare.urad_api.containers.standard import Container
from application.models import *
from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        variations = Variation.objects.all()
        print "[*]================> Update static variation \n"
        for variation in variations:
            gene = VariationAssociatedGene.objects.filter(variation_id= variation.id).count()
            disease = VariationAssociatedDisease.objects.filter(variation_id= variation.id).count()
            pub = VariationAssociatedPublication.objects.filter(variation_id= variation.id).count()

            variation.num_associated_gene = gene
            variation.num_associated_disease = disease
            variation.num_associated_publication = pub
            variation.save()
            print "="*10+ " Done " + variation.title+ "\n"



        genes = Gene.objects.all()
        print "[*]================> Update static variation \n"
        for gene in genes:
            disease = GeneAssociatedDisease.objects.filter(gene_id= gene.id).count()
            pub = GeneAssociatedPublication.objects.filter(gene_id= gene.id).count()

            gene.num_associated_disease = disease
            gene.num_associated_publication = pub
            gene.save()
            print "="*10+ " Done " + gene.title+ "\n"
