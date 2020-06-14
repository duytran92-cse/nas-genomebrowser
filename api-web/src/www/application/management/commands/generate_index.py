from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from application.models import *

class Command(BaseCommand):
    help = 'Build search index database'

    def handle(self, *args, **kwargs):
        # Clear up database
        SearchIndex.objects.all().delete()

        ctype = ['variation', 'disease', 'gene', 'trait', 'treatment']
        # Index
        for i in ctype:
            print i + " inprocess"
            alias = None
            if i == 'variation':
                data = Variation.objects.filter(is_disabled=False).all()
            elif i == 'disease':
                data = Disease.objects.filter(is_disabled=False).all()
            elif i == 'gene':
                data = Gene.objects.filter(is_disabled=False).all()
            elif i == 'trait':
                data = Trait.objects.filter(is_disabled=False).all()
            elif i == 'treatment':
                data = Treatment.objects.filter(is_disabled=False).all()
            else:
                pass
            if data:
                search_indexes = []
                search_names = []
                for v in data:
                    if  v.title not in search_names:
                        search_index = SearchIndex()
                        search_index.name = v.title
                        search_index.ctype = i
                        search_index.reference = ''
                        search_indexes.append(search_index)
                        search_names.append(search_index.name)

                        # Get alias name
                        if i == 'variation':
                            alias_version = VariationBlockAliasVersion.objects.filter(is_disabled=False, is_stable=True, version_status='active', variation_id=v.id).order_by('-created_at')[:1]
                            if alias_version:
                                for item in alias_version:
                                    alias = VariationBlockAlias.objects.filter(variation_block_version_id=item.id)
                        elif i == 'disease':
                            alias_version = DiseaseBlockAliasVersion.objects.filter(is_disabled=False, is_stable=True, version_status='active', disease_id=v.id).order_by('-created_at')[:1]
                            if alias_version:
                                for item in alias_version:
                                    alias = DiseaseBlockAlias.objects.filter(disease_block_version_id=item.id)
                        elif i == 'gene':
                            alias_version = GeneBlockAliasVersion.objects.filter(is_disabled=False, is_stable=True, version_status='active', gene_id=v.id).order_by('-created_at')[:1]
                            if alias_version:
                                for item in alias_version:
                                    alias = GeneBlockAlias.objects.filter(gene_block_version_id=item.id)
                        elif i == 'trait':
                            alias_version = TraitBlockAliasVersion.objects.filter(is_disabled=False, is_stable=True, version_status='active', trait_id=v.id).order_by('-created_at')[:1]
                            if alias_version:
                                for item in alias_version:
                                    alias = TraitBlockAlias.objects.filter(trait_block_version_id=item.id)
                        elif i == 'treatment':
                            alias_version = TreatmentBlockAliasVersion.objects.filter(is_disabled=False, is_stable=True, version_status='active', treatment_id=v.id).order_by('-created_at')[:1]
                            if alias_version:
                                for item in alias_version:
                                    alias = TreatmentBlockAlias.objects.filter(treatment_block_version_id=item.id)
                        else:
                            pass

                        if alias:
                            for item in alias:
                                if item.alias not in search_names:
                                    synonym = SearchIndex()
                                    synonym.name = item.alias
                                    synonym.ctype = i
                                    synonym.reference = search_index.name
                                    search_indexes.append(synonym)
                                    search_names.append(item.alias)
                SearchIndex.objects.bulk_create(search_indexes)
                print i + " Done"
            else:
                print i + ' No data found'
