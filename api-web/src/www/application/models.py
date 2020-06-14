from __future__ import unicode_literals
from django.db import models
from django.db.models import Max
from . import constants


class Page(models.Model):
    title = models.TextField(default='')
    content = models.TextField(default='')
    is_disabled = models.BooleanField(default=False)

class ApplicationSetting(models.Model):
    application_title = models.CharField(max_length=255, default='')
    contact_address_text = models.TextField(default='')
    about_genopedia_text = models.TextField(default='')
    facebook_url = models.CharField(max_length=255, default='')
    twitter_url = models.CharField(max_length=255, default='')
    youtube_url = models.CharField(max_length=255, default='')
    linkedin_url = models.CharField(max_length=255, default='')
    google_plus_url = models.CharField(max_length=255, default='')
    impression_page = models.ForeignKey('Page', related_name='impression_page', null=True)
    privacy_page = models.ForeignKey('Page', related_name='privacy_page', null=True)
    copyright_page = models.ForeignKey('Page', related_name='copyright_page', null=True)
    term_of_use_page = models.ForeignKey('Page', related_name='term_of_use_page', null=True)
    stat_num_variation = models.IntegerField(default=0)
    stat_num_gene = models.IntegerField(default=0)
    stat_num_disease = models.IntegerField(default=0)
    stat_num_disease_causing_mutation = models.IntegerField(default=0)
    stat_num_trait = models.IntegerField(default=0)
    stat_num_drug = models.IntegerField(default=0)
    stat_num_treatment = models.IntegerField(default=0)
    stat_num_cited_publication = models.IntegerField(default=0)
    stat_num_page = models.IntegerField(default=0)
    stat_num_registered_user = models.IntegerField(default=0)
    stat_num_genetic_code_letter = models.IntegerField(default=0)
    stat_num_forum_post = models.IntegerField(default=0)

# Variation
class EmailSubscribe(models.Model):
    email = models.TextField(default='')

# Variation
class Variation(models.Model):
    title = models.TextField(default='')
    num_associated_gene = models.IntegerField(default=0)
    num_associated_disease = models.IntegerField(default=0)
    num_associated_publication = models.IntegerField(default=0)
    is_disabled = models.BooleanField(default=False)

class VariationGenotype(models.Model):
    variation = models.ForeignKey('Variation')
    genotype = models.CharField(max_length=10, default='')
    box_color = models.CharField(max_length=50, default='')
    source = models.TextField(default='')

class VariationAssociatedGene(models.Model):
    variation = models.ForeignKey('Variation')
    gene_name = models.CharField(max_length=50, default='')
    is_disabled = models.BooleanField(default=False)

class VariationAssociatedDisease(models.Model):
    variation = models.ForeignKey('Variation')
    disease_name = models.CharField(max_length=50, default='')
    is_disabled = models.BooleanField(default=False)

class VariationAssociatedPublication(models.Model):
    variation = models.ForeignKey('Variation')
    pmid = models.CharField(max_length=50, default='')
    doi = models.CharField(max_length=50, default='')
    pmc = models.CharField(max_length=50, default='')
    title = models.CharField(max_length=1024, default='')
    authors = models.TextField(default='')
    journal = models.CharField(max_length=1024, default='')
    is_disabled = models.BooleanField(default=False)

class VariationBlock(models.Model):
    variation = models.ForeignKey('Variation')
    kind = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_KINDS)
    position = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_POSITIONS)
    title = models.TextField(default='')
    text = models.TextField(default='')
    sort_order = models.IntegerField(default=0)
    is_disabled = models.BooleanField(default=False)

class VariationBlockPublicationVersion(models.Model):
    variation = models.ForeignKey('Variation')
    variation_block = models.ForeignKey('VariationBlock')
    title = models.TextField(default='')
    text = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=50, default='', choices=constants.USERS)
    version = models.IntegerField(default=1)
    version_status = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_VERSION_STATUS)
    is_disabled = models.BooleanField(default=False)
    is_stable = models.BooleanField(default=False)

class VariationBlockPublication(models.Model):
    variation_block = models.ForeignKey('VariationBlock')
    variation_block_version = models.ForeignKey('VariationBlockPublicationVersion')
    pmid = models.CharField(max_length=50, default='')
    doi = models.CharField(max_length=50, default='')
    pmc = models.CharField(max_length=50, default='')
    title = models.CharField(max_length=1024, default='')
    authors = models.TextField(default='')
    journal = models.CharField(max_length=1024, default='')

class VariationBlockPublicationTextVersion(models.Model):
    variation = models.ForeignKey('Variation')
    variation_block = models.ForeignKey('VariationBlock')
    title = models.TextField(default='')
    text = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=50, default='', choices=constants.USERS)
    version = models.IntegerField(default=1)
    version_status = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_VERSION_STATUS)
    is_disabled = models.BooleanField(default=False)
    is_stable = models.BooleanField(default=False)

class VariationBlockPublicationText(models.Model):
    variation_block = models.ForeignKey('VariationBlock')
    variation_block_version = models.ForeignKey('VariationBlockPublicationTextVersion')
    title = models.CharField(max_length=1024, default='')
    sentence = models.TextField(default='')
    pubmedid = models.CharField(max_length=50, default='')

class VariationBlockAlias(models.Model):
    variation_block = models.ForeignKey('VariationBlock')
    variation_block_version = models.ForeignKey('VariationBlockAliasVersion')
    alias = models.CharField(max_length=255, default='')

class VariationBlockAliasVersion(models.Model):
    variation = models.ForeignKey('Variation')
    variation_block = models.ForeignKey('VariationBlock')
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=50, default='', choices=constants.USERS)
    version = models.IntegerField(default=1)
    version_status = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_VERSION_STATUS)
    is_disabled = models.BooleanField(default=False)
    is_stable = models.BooleanField(default=False)

class VariationBlockDisgenetDiseases(models.Model):
    variation_block = models.ForeignKey('VariationBlock')
    variation_block_version = models.ForeignKey('VariationBlockDisgenetDiseasesVersion')
    title = models.CharField(max_length=255, default='')
    pubmedid = models.CharField(max_length=50, default='')
    sentence = models.TextField(default='')

class VariationBlockDisgenetDiseasesVersion(models.Model):
    variation = models.ForeignKey('Variation')
    variation_block = models.ForeignKey('VariationBlock')
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=50, default='', choices=constants.USERS)
    version = models.IntegerField(default=1)
    version_status = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_VERSION_STATUS)
    is_disabled = models.BooleanField(default=False)
    is_stable = models.BooleanField(default=False)

class VariationBlockInfobox(models.Model):
    variation_block = models.ForeignKey('VariationBlock')
    variation_block_version = models.ForeignKey('VariationBlockInfoboxVersion')
    key = models.CharField(max_length=255, default='')
    value = models.TextField(default='')

class VariationBlockInfoboxVersion(models.Model):
    variation = models.ForeignKey('Variation')
    variation_block = models.ForeignKey('VariationBlock')
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=50, default='', choices=constants.USERS)
    version = models.IntegerField(default=1)
    version_status = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_VERSION_STATUS)
    is_disabled = models.BooleanField(default=False)
    is_stable = models.BooleanField(default=False)

class VariationBlockFrequency(models.Model):
    variation_block = models.ForeignKey('VariationBlock')
    variation_block_version = models.ForeignKey('VariationBlockFrequencyVersion')
    popcode = models.CharField(max_length=50, default='', choices=constants.POPULATION_CODES)
    genotype_count_00 = models.IntegerField(default=0)
    genotype_count_01 = models.IntegerField(default=0)
    genotype_count_11 = models.IntegerField(default=0)

class VariationBlockFrequencyVersion(models.Model):
    variation = models.ForeignKey('Variation')
    variation_block = models.ForeignKey('VariationBlock')
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=50, default='', choices=constants.USERS)
    version = models.IntegerField(default=1)
    version_status = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_VERSION_STATUS)
    is_disabled = models.BooleanField(default=False)
    is_stable = models.BooleanField(default=False)

class VariationBlockEffectVersion(models.Model):
    variation = models.ForeignKey('Variation')
    variation_block = models.ForeignKey('VariationBlock')
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=50, default='', choices=constants.USERS)
    version = models.IntegerField(default=1)
    version_status = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_VERSION_STATUS)
    is_disabled = models.BooleanField(default=False)
    is_stable = models.BooleanField(default=False)


class VariationBlockEffect(models.Model):
    variation_block = models.ForeignKey('VariationBlock')
    variation_block_version = models.ForeignKey('VariationBlockEffectVersion')
    popcode = models.CharField(max_length=50, default='', choices=constants.POPULATION_CODES)
    genotype = models.CharField(max_length=10, default='')
    risk = models.TextField(default='')
    odd_ratio = models.FloatField(default=0)
    evidences = models.TextField(default='')
    pmid = models.CharField(max_length=50, default='')

class VariationEffectNote(models.Model):
    risk = models.TextField(default='')
    popcode =  models.TextField(default='')
    genotype =  models.TextField(default='')
    risk =  models.TextField(default='')
    odd_ratio =  models.TextField(default='')
    evidences =  models.TextField(default='')
    pmid =  models.TextField(default='')

class VariationBlockVersion(models.Model):
    variation = models.ForeignKey('Variation')
    variation_block = models.ForeignKey('VariationBlock')
    title = models.TextField(default='')
    text = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=50, default='', choices=constants.USERS)
    version = models.IntegerField(default=1)
    version_status = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_VERSION_STATUS)
    is_disabled = models.BooleanField(default=False)
    is_stable = models.BooleanField(default=False)

# Gene
class Gene(models.Model):
    title = models.TextField(default='')
    is_disabled = models.BooleanField(default=False)
    num_associated_disease = models.IntegerField(default=0)
    num_associated_publication = models.IntegerField(default=0)

class GeneAssociatedDisease(models.Model):
    gene = models.ForeignKey('Gene')
    disease_name = models.CharField(max_length=100, default='')
    is_disabled = models.BooleanField(default=False)

class GeneAssociatedPublication(models.Model):
    gene = models.ForeignKey('Gene')
    pmid = models.CharField(max_length=50, default='')
    doi = models.CharField(max_length=50, default='')
    pmc = models.CharField(max_length=50, default='')
    title = models.CharField(max_length=1024, default='')
    authors = models.TextField(default='')
    journal = models.CharField(max_length=1024, default='')
    is_disabled = models.BooleanField(default=False)

class GeneBlockVersion(models.Model):
    gene = models.ForeignKey('Gene')
    gene_block = models.ForeignKey('GeneBlock')
    title = models.TextField(default='')
    text = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=50, default='', choices=constants.USERS)
    version = models.IntegerField(default=1)
    version_status = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_VERSION_STATUS)
    is_disabled = models.BooleanField(default=False)
    is_stable = models.BooleanField(default=False)

class GeneBlock(models.Model):
    gene = models.ForeignKey('Gene')
    kind = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_KINDS)
    position = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_POSITIONS)
    title = models.TextField(default='')
    text = models.TextField(default='')
    sort_order = models.IntegerField(default=0)
    is_disabled = models.BooleanField(default=False)


class GeneBlockPublicationVersion(models.Model):
    gene = models.ForeignKey('Gene')
    gene_block = models.ForeignKey('GeneBlock')
    title = models.TextField(default='')
    text = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=50, default='', choices=constants.USERS)
    version = models.IntegerField(default=1)
    version_status = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_VERSION_STATUS)
    is_disabled = models.BooleanField(default=False)
    is_stable = models.BooleanField(default=False)

class GeneBlockPublication(models.Model):
    gene_block = models.ForeignKey('GeneBlock')
    gene_block_version = models.ForeignKey('GeneBlockPublicationVersion')
    pmid = models.CharField(max_length=50, default='')
    doi = models.CharField(max_length=50, default='')
    pmc = models.CharField(max_length=50, default='')
    title = models.CharField(max_length=1024, default='')
    authors = models.TextField(default='')
    journal = models.CharField(max_length=1024, default='')

class GeneBlockEffectVersion(models.Model):
    gene = models.ForeignKey('Gene')
    gene_block = models.ForeignKey('GeneBlock')
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=50, default='', choices=constants.USERS)
    version = models.IntegerField(default=1)
    version_status = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_VERSION_STATUS)
    is_disabled = models.BooleanField(default=False)
    is_stable = models.BooleanField(default=False)

class GeneBlockEffect(models.Model):
    gene_block = models.ForeignKey('GeneBlock')
    gene_block_version = models.ForeignKey('GeneBlockEffectVersion')
    type = models.CharField(max_length=100, default='', choices=constants.GENE_EFFECT_TYPE)
    effect = models.TextField(default='')
    evidences = models.TextField(default='')
    publication = models.TextField(default='')

class GeneBlockAlias(models.Model):
    gene_block = models.ForeignKey('GeneBlock')
    gene_block_version = models.ForeignKey('GeneBlockAliasVersion')
    alias = models.CharField(max_length=255, default='')

class GeneBlockAliasVersion(models.Model):
    gene = models.ForeignKey('Gene')
    gene_block = models.ForeignKey('GeneBlock')
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=50, default='', choices=constants.USERS)
    version = models.IntegerField(default=1)
    version_status = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_VERSION_STATUS)
    is_disabled = models.BooleanField(default=False)
    is_stable = models.BooleanField(default=False)

class GeneBlockInfobox(models.Model):
    gene_block = models.ForeignKey('GeneBlock')
    gene_block_version = models.ForeignKey('GeneBlockInfoboxVersion')
    description = models.TextField(default='')
    chromosome = models.CharField(max_length=100, default='')
    start = models.IntegerField(default=0)
    end = models.IntegerField(default=0)
    number_of_exons = models.IntegerField(default=0)
    protein_products = models.CharField(max_length=255, default='')

class GeneBlockInfoboxVersion(models.Model):
    gene = models.ForeignKey('Gene')
    gene_block = models.ForeignKey('GeneBlock')
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=50, default='', choices=constants.USERS)
    version = models.IntegerField(default=1)
    version_status = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_VERSION_STATUS)
    is_disabled = models.BooleanField(default=False)
    is_stable = models.BooleanField(default=False)

# Trait
class Trait(models.Model):
    title = models.TextField(default='')
    is_disabled = models.BooleanField(default=False)

class TraitBlockVersion(models.Model):
    trait = models.ForeignKey('Trait')
    trait_block = models.ForeignKey('TraitBlock')
    title = models.TextField(default='')
    text = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=50, default='', choices=constants.USERS)
    version = models.IntegerField(default=1)
    version_status = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_VERSION_STATUS)
    is_disabled = models.BooleanField(default=False)
    is_stable = models.BooleanField(default=False)

class TraitBlock(models.Model):
    trait = models.ForeignKey('Trait')
    kind = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_KINDS)
    position = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_POSITIONS)
    title = models.TextField(default='')
    text = models.TextField(default='')
    sort_order = models.IntegerField(default=0)
    is_disabled = models.BooleanField(default=False)

class TraitBlockPublicationVersion(models.Model):
    trait = models.ForeignKey('Trait')
    trait_block = models.ForeignKey('TraitBlock')
    title = models.TextField(default='')
    text = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=50, default='', choices=constants.USERS)
    version = models.IntegerField(default=1)
    version_status = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_VERSION_STATUS)
    is_disabled = models.BooleanField(default=False)
    is_stable = models.BooleanField(default=False)

class TraitBlockPublication(models.Model):
    trait_block = models.ForeignKey('TraitBlock')
    trait_block_version = models.ForeignKey('TraitBlockPublicationVersion')
    pmid = models.CharField(max_length=50, default='')
    doi = models.CharField(max_length=50, default='')
    pmc = models.CharField(max_length=50, default='')
    title = models.CharField(max_length=1024, default='')
    authors = models.TextField(default='')
    journal = models.CharField(max_length=1024, default='')

class TraitBlockAlias(models.Model):
    trait_block = models.ForeignKey('TraitBlock')
    trait_block_version = models.ForeignKey('TraitBlockAliasVersion')
    alias = models.CharField(max_length=255, default='')

class TraitBlockAliasVersion(models.Model):
    trait = models.ForeignKey('Trait')
    trait_block = models.ForeignKey('TraitBlock')
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=50, default='', choices=constants.USERS)
    version = models.IntegerField(default=1)
    version_status = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_VERSION_STATUS)
    is_disabled = models.BooleanField(default=False)
    is_stable = models.BooleanField(default=False)

# Disease
class Disease(models.Model):
    title = models.TextField(default='')
    is_disabled = models.BooleanField(default=False)

class DiseaseAssociatedGene(models.Model):
    disease = models.ForeignKey('Disease')
    gene_name = models.CharField(max_length=50, default='')
    is_disabled = models.BooleanField(default=False)

class DiseaseAssociatedPublication(models.Model):
    disease = models.ForeignKey('Disease')
    pmid = models.CharField(max_length=50, default='')
    doi = models.CharField(max_length=50, default='')
    pmc = models.CharField(max_length=50, default='')
    title = models.CharField(max_length=1024, default='')
    authors = models.TextField(default='')
    journal = models.CharField(max_length=1024, default='')
    is_disabled = models.BooleanField(default=False)

class DiseaseBlock(models.Model):
    disease = models.ForeignKey('Disease')
    kind = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_KINDS)
    position = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_POSITIONS)
    title = models.TextField(default='')
    text = models.TextField(default='')
    sort_order = models.IntegerField(default=0)
    is_disabled = models.BooleanField(default=False)

class DiseaseBlockPublicationVersion(models.Model):
    disease = models.ForeignKey('Disease')
    disease_block = models.ForeignKey('DiseaseBlock')
    title = models.TextField(default='')
    text = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=50, default='', choices=constants.USERS)
    version = models.IntegerField(default=1)
    version_status = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_VERSION_STATUS)
    is_disabled = models.BooleanField(default=False)
    is_stable = models.BooleanField(default=False)

class DiseaseBlockPublication(models.Model):
    disease_block = models.ForeignKey('DiseaseBlock')
    disease_block_version = models.ForeignKey('DiseaseBlockPublicationVersion')
    pmid = models.CharField(max_length=50, default='')
    doi = models.CharField(max_length=50, default='')
    pmc = models.CharField(max_length=50, default='')
    title = models.CharField(max_length=1024, default='')
    authors = models.TextField(default='')
    journal = models.CharField(max_length=1024, default='')

class DiseaseBlockVersion(models.Model):
    disease = models.ForeignKey('Disease')
    disease_block = models.ForeignKey('DiseaseBlock')
    title = models.TextField(default='')
    text = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=50, default='', choices=constants.USERS)
    version = models.IntegerField(default=1)
    version_status = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_VERSION_STATUS)
    is_disabled = models.BooleanField(default=False)
    is_stable = models.BooleanField(default=False)

class DiseaseBlockAlias(models.Model):
    disease_block = models.ForeignKey('DiseaseBlock')
    disease_block_version = models.ForeignKey('DiseaseBlockAliasVersion')
    alias = models.CharField(max_length=255, default='')

class DiseaseBlockAliasVersion(models.Model):
    disease = models.ForeignKey('Disease')
    disease_block = models.ForeignKey('DiseaseBlock')
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=50, default='', choices=constants.USERS)
    version = models.IntegerField(default=1)
    version_status = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_VERSION_STATUS)
    is_disabled = models.BooleanField(default=False)
    is_stable = models.BooleanField(default=False)

# Treatment
class Treatment(models.Model):
    title = models.TextField(default='')
    is_disabled = models.BooleanField(default=False)

class TreatmentBlock(models.Model):
    treatment = models.ForeignKey('Treatment')
    kind = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_KINDS)
    position = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_POSITIONS)
    title = models.TextField(default='')
    text = models.TextField(default='')
    sort_order = models.IntegerField(default=0)
    is_disabled = models.BooleanField(default=False)

class TreatmentBlockPublicationVersion(models.Model):
    treatment = models.ForeignKey('Treatment')
    treatment_block = models.ForeignKey('TreatmentBlock')
    title = models.TextField(default='')
    text = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=50, default='', choices=constants.USERS)
    version = models.IntegerField(default=1)
    version_status = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_VERSION_STATUS)
    is_disabled = models.BooleanField(default=False)
    is_stable = models.BooleanField(default=False)

class TreatmentBlockPublication(models.Model):
    treatment_block = models.ForeignKey('TreatmentBlock')
    treatment_block_version = models.ForeignKey('TreatmentBlockPublicationVersion')
    pmid = models.CharField(max_length=50, default='')
    doi = models.CharField(max_length=50, default='')
    pmc = models.CharField(max_length=50, default='')
    title = models.CharField(max_length=1024, default='')
    authors = models.TextField(default='')
    journal = models.CharField(max_length=1024, default='')

class TreatmentBlockVersion(models.Model):
    treatment = models.ForeignKey('Treatment')
    treatment_block = models.ForeignKey('TreatmentBlock')
    title = models.TextField(default='')
    text = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=50, default='', choices=constants.USERS)
    version = models.IntegerField(default=1)
    version_status = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_VERSION_STATUS)
    is_disabled = models.BooleanField(default=False)
    is_stable = models.BooleanField(default=False)

class TreatmentBlockAlias(models.Model):
    treatment_block = models.ForeignKey('TreatmentBlock')
    treatment_block_version = models.ForeignKey('TreatmentBlockAliasVersion')
    alias = models.CharField(max_length=255, default='')

class TreatmentBlockAliasVersion(models.Model):
    treatment = models.ForeignKey('Treatment')
    treatment_block = models.ForeignKey('TreatmentBlock')
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=50, default='', choices=constants.USERS)
    version = models.IntegerField(default=1)
    version_status = models.CharField(max_length=50, default='', choices=constants.PAGE_BLOCK_VERSION_STATUS)
    is_disabled = models.BooleanField(default=False)
    is_stable = models.BooleanField(default=False)

class User(models.Model):
    email = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    password = models.TextField(default='')
    salt = models.TextField(default='')
    id_type = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)

class UserInformation(models.Model):
    user = models.ForeignKey('User')
    fullname = models.TextField(default='')
    position = models.TextField(default='')
    about = models.TextField(default='')
    gender = models.IntegerField(default=0)
    country = models.CharField(max_length=45,default='')
    education = models.TextField(default='')
    work = models.TextField(default='')
    photo = models.TextField(default='')
    rank_place = models.IntegerField(default=0)
    age = models.IntegerField(default=0)
    account_paypal = models.TextField(default='')

class Comment(models.Model):
    user = models.ForeignKey('User')
    page = models.CharField(max_length=255, default='')
    comment = models.TextField(default='')
    timestamp = models.DateTimeField(auto_now=True)
    root = models.IntegerField(default=0)
    numLike = models.IntegerField(default=0)
    entity = models.CharField(max_length=255, default='')

class CommentUserLike(models.Model):
    user = models.ForeignKey('User')
    comment = models.ForeignKey('Comment')

class SearchIndex(models.Model):
    name = models.CharField(max_length=255)
    ctype = models.CharField(max_length=50)
    reference = models.CharField(max_length=255,null=True)

class ContactUs(models.Model):
    email = models.CharField(max_length=255)
    message = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now=True)

class TextBlock(models.Model):
    text = models.TextField(default='')
    text_code = models.TextField(default='')
    kind = models.CharField(max_length=50,default='')
    is_disabled = models.BooleanField(default=False)

class Language(models.Model):
    code = models.CharField(max_length=10,default='')
    title = models.CharField(max_length=50,default='')
    is_disabled = models.BooleanField(default=False)

class TextBlockLanguage(models.Model):
    text_block = models.ForeignKey('TextBlock')
    language = models.CharField(max_length=50,default='')
    translate = models.TextField(default='')

class Popcode(models.Model):
    popcode = models.CharField(max_length=50,default='')
    parent = models.CharField(max_length=50,default='')
    name = models.CharField(max_length=50,default='')
