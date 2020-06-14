from django.conf.urls import include, url

urlpatterns = [
    url(r'^page/',                           include('application.modules.page.urls')),
    url(r'^application_setting/',            include('application.modules.application_setting.urls')),
    url(r'^text_block/',                     include('application.modules.text_block.urls')),
    url(r'^language/',                       include('application.modules.language.urls')),

    url(r'^variation/',                      include('application.modules.variation.urls')),
    url(r'^variation_block/',                include('application.modules.variation_block.urls')),
    url(r'^variation_block_version/',        include('application.modules.variation_block_version.urls')),
    url(r'^variation_block_pub_version/',    include('application.modules.variation_block_pub_version.urls')),
    url(r'^variation_block_pub_text_version/',include('application.modules.variation_block_pub_text_version.urls')),
    url(r'^variation_block_eff_version/',    include('application.modules.variation_block_eff_version.urls')),
    url(r'^variation_block_alias_version/',  include('application.modules.variation_block_alias_version.urls')),
    url(r'^variation_block_fre_version/',    include('application.modules.variation_block_fre_version.urls')),
    url(r'^variation_block_infobox_version/',include('application.modules.variation_block_infobox_version.urls')),
    url(r'^variation_block_disgenet_version/',include('application.modules.variation_block_disgenet_diseases_version.urls')),

    url(r'^disease/',                        include('application.modules.disease.urls')),
    url(r'^disease/',                        include('application.modules.disease.urls')),
    url(r'^disease_block/',                  include('application.modules.disease_block.urls')),
    url(r'^disease_block_version/',          include('application.modules.disease_block_version.urls')),
    url(r'^disease_block_pub_version/',      include('application.modules.disease_block_pub_version.urls')),
    url(r'^disease_block_alias_version/',    include('application.modules.disease_block_alias_version.urls')),

    url(r'^gene/',                           include('application.modules.gene.urls')),
    url(r'^gene_block/',                     include('application.modules.gene_block.urls')),
    url(r'^gene_block_version/',             include('application.modules.gene_block_version.urls')),
    url(r'^gene_block_pub_version/',         include('application.modules.gene_block_pub_version.urls')),
    url(r'^gene_block_eff_version/',         include('application.modules.gene_block_eff_version.urls')),
    url(r'^gene_block_alias_version/',       include('application.modules.gene_block_alias_version.urls')),
    url(r'^gene_block_infobox_version/',     include('application.modules.gene_block_infobox_version.urls')),

    url(r'^trait/',                          include('application.modules.trait.urls')),
    url(r'^trait_block/',                    include('application.modules.trait_block.urls')),
    url(r'^trait_block_version/',            include('application.modules.trait_block_version.urls')),
    url(r'^trait_block_pub_version/',        include('application.modules.trait_block_pub_version.urls')),
    url(r'^trait_block_alias_version/',      include('application.modules.trait_block_alias_version.urls')),

    url(r'^treatment/',                      include('application.modules.treatment.urls')),
    url(r'^treatment_block/',                include('application.modules.treatment_block.urls')),
    url(r'^treatment_block_version/',        include('application.modules.treatment_block_version.urls')),
    url(r'^treatment_block_pub_version/',    include('application.modules.treatment_block_pub_version.urls')),
    url(r'^treatment_block_alias_version/',  include('application.modules.treatment_block_alias_version.urls')),

    url(r'^email_subscribe/',                 include('application.modules.email_subscribe.urls')),

    url(r'^comment/',                        include('application.modules.comment.urls')),
]
