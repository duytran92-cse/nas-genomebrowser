from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from notasquare.urad_api.containers.standard import Container
from application.models import *
from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # records = [
        #     {'rs3': {'position': 1000, 'synonyms': 'value', 'is_somatic': True}},
        #     {'rs4': {'position': 1000, 'synonyms': 'value', 'is_somatic': True}},
        # ]
        params = {}
        params['_pagernum'] = 10
        params['_sort_key'] = 'id'
        params['_sort_dir'] = 'desc'

        ## VARIATION
        isDone = False
        page = 1
        while not isDone:
            params['_pageroffset'] = (page - 1) * 10
            _variation = Container().call_api(settings.GENODATA_API_URL + '/variation/list_detail', GET=params)
            # _variation = Container().call_api('http://genodata-api.gp.test.notasquare.vn/variation/list_detail', GET=params)
            variation_records = _variation['records']
            page += 1
            if len(variation_records) == 0:
                isDone = True
            variation_genotypes = []
            variation_genes = []
            variation_pubs = []
            # Start for
            for item in variation_records:
                variation = Variation()
                variation.title = item.keys()[0]
                variation.save()

                variation_genotype = VariationBlockGenotype(variation_id=variation.id)
                variation_genotype.genotype = item.values()[0].get('genotype','')
                variation_genotype.box_color = item.values()[0].get('box_color','')
                variation_genotypes.append(variation_genotype)

                if 'gene' in item.values()[0]:
                    for g in item.values()[0]['gene']:
                        variation_gene = VariationAssociatedGene(variation_id=variation.id)
                        variation_gene.gene_name = g
                        variation_genes.append(variation_gene)

                if 'publication' in item.values()[0]:
                    for p in item.values()[0]['publication']:
                        variation_pub = VariationAssociatedPublication(variation_id=variation.id)
                        variation_pub.pmid = p['pmid']
                        variation_pub.doi = p['doi']
                        variation_pub.pmc = p['pmc']
                        variation_pub.title = p['title']
                        variation_pub.authors = p['authors']
                        variation_pub.journal = p['journal']
                        variation_pubs.append(variation_pub)
            # End for
            if variation_genotypes:
                VariationBlockGenotype.objects.bulk_create(variation_genotypes)
            if variation_genes:
                VariationAssociatedGene.objects.bulk_create(variation_genes)
            if variation_pubs:
                VariationAssociatedPublication.objects.bulk_create(variation_pubs)
        ## END VARIATION

        ## GENE
        isDone = False
        page = 1
        while not isDone:
            params['_pageroffset'] = (page - 1) * 10
            _gene =  Container().call_api(settings.GENODATA_API_URL + '/gene/list_detail', GET=params)
            gene_records = _gene['records']
            page += 1
            if len(gene_records) == 0:
                isDone = True
            gene_records = []
            gene_diseases = []
            # Start for
            for item in gene_records:
                gene = Gene()
                gene.title = item.keys()[0]
                gene.save()

                if 'disease' in item.values()[0]:
                    for d in item.values()[0]['disease']:
                        gene_disease = GeneAssociatedDisease(gene_id=gene.id)
                        gene_disease.disease_name = d
                        gene_diseases.append(gene_disease)

            if gene_diseases:
                GeneAssociatedDisease.objects.bulk_create(gene_diseases)
        ## END GENE

        ## TRAIT
        isDone = False
        page = 1
        while not isDone:
            params['_pageroffset'] = (page - 1) * 10
            _trait =  Container().call_api(settings.GENODATA_API_URL + '/trait/list_detail', GET=params)
            trait_records = _trait['records']
            page += 1
            if len(trait_records) == 0:
                isDone = True
            traits = []
            # Start for
            for item in trait_records:
                trait = Trait()
                trait.title = item.keys()[0]
                traits.append(trait)
            if traits:
                Trait.objects.bulk_create(traits)
        ## END TRAIT

        ## DISEASE
        isDone = False
        page = 1
        while not isDone:
            params['_pageroffset'] = (page - 1) * 10
            _disease =  Container().call_api(settings.GENODATA_API_URL + '/disease/list_detail', GET=params)
            disease_records = _disease['records']
            page += 1
            if len(disease_records) == 0:
                isDone = True
            disease_genes = []
            disease_pubs = []
            # Start for
            for item in disease_records:
                disease = Trait()
                disease.title = item.keys()[0]
                disease.save()

                if 'gene' in item.values()[0]:
                    for g in item.values()[0]['gene']:
                        disease_gene = DiseaseAssociatedGene(disease_id=disease.id)
                        disease_gene.gene_name = g
                        disease_genes.append(disease_gene)

                if 'publication' in item.values()[0]:
                    for p in item.values()[0]['publication']:
                        disease_pub = DiseaseAssociatedPublication(disease_id=disease.id)
                        disease_pub.pmid = p['pmid']
                        disease_pub.doi = p['doi']
                        disease_pub.pmc = p['pmc']
                        disease_pub.title = p['title']
                        disease_pub.authors = p['authors']
                        disease_pub.journal = p['journal']
                        disease_pubs.append(disease_pub)

            if disease_genes:
                DiseaseAssociatedGene.objects.bulk_create(disease_genes)
            if disease_pubs:
                DiseaseAssociatedPublication.objects.bulk_create(disease_pubs)
        ## END DISEASE

        ## TREATMENT
        isDone = False
        page = 1
        while not isDone:
            params['_pageroffset'] = (page - 1) * 10
            _treatment =  Container().call_api(settings.GENODATA_API_URL + '/treatment/list_detail', GET=params)
            treatment_records = _treatment['records']
            page += 1
            if len(treatment_records) == 0:
                isDone = True
            treatments = []
            # Start for
            for item in treatment_records:
                treatment = Treatment()
                treatment.title = item.keys()[0]
                treatments.append(treatment)

            if treatments:
                Treatment.objects.bulk_create(treatments)
        ## END TREATMENT
