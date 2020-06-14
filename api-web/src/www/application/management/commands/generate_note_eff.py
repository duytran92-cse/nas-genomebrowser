from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from application.models import *

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        query = VariationEffectNote.objects.filter()
        if query:
            note = query[0]
        else:
            note = VariationEffectNote()
        note.popcode = 'Popcode'
        note.genotype = 'Genotype'
        note.risk = 'Risk'
        note.odd_ratio = 'Odd ratio'
        note.evidences = 'Evidences'
        note.pmid = 'Pmid'
        note.save()
        print "**************==> Done!"
