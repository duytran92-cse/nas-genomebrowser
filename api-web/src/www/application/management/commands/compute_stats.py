from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from application.models import *

class Command(BaseCommand):
    help = 'Build search index database'
    def get_application_setting(self):
        records = ApplicationSetting.objects.all()
        for r in records:
            return r
        application_setting = ApplicationSetting()
        application_setting.save()
        return application_setting

    def handle(self, *args, **kwargs):
        print 'start inserting'

        # Insert data
        num_variation = Variation.objects.filter(is_disabled=False).count()
        num_gene = Gene.objects.filter(is_disabled=False).count()
        num_disease = Disease.objects.filter(is_disabled=False).count()
        num_trait = Trait.objects.filter(is_disabled=False).count()
        num_treatment = Treatment.objects.filter(is_disabled=False).count()
        num_drug = 0
        num_disease_causing_mutation = 0
        registeredUsers = User.objects.all().count()
        pages = num_trait + num_treatment + num_gene + num_disease + num_variation
        geneticCodeLetters = 64696600

        # Index
        application = self.get_application_setting()
        application.stat_num_variation = num_variation
        application.stat_num_gene = num_gene
        application.stat_num_disease = num_disease
        application.stat_num_trait = num_trait
        application.stat_num_treatment = num_treatment
        application.stat_num_drug = num_drug
        application.stat_num_disease_causing_mutation = num_disease_causing_mutation
        application.stat_num_registered_user = registeredUsers
        application.stat_num_page = pages
        application.stat_num_genetic_code_letter = geneticCodeLetters

        application.save()
        print "Done"
