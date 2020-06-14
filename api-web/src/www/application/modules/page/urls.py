
from django.conf.urls import include, url
from . import handlers

urlpatterns = [
    url(r'^get$',                           handlers.Get.as_view(),                 name='page_get'),
    url(r'^list$',                          handlers.List.as_view(),                name='page_list'),
    url(r'^create$',                        handlers.Create.as_view(),              name='page_create'),
    url(r'^update$',                        handlers.Update.as_view(),              name='page_update'),
    url(r'^delete$',                        handlers.Delete.as_view(),              name='page_delete'),
    url(r'^get_content_page$',              handlers.GetContentPage.as_view(),      name='page_get_content_page'),
    url(r'^dashboard$',                     handlers.Dashboard.as_view(),           name='dashboard'),
    url(r'^unstable_blocks$',               handlers.UnstableBlocks.as_view(),      name='unstable_blocks'),
    url(r'^list_blocks$',                   handlers.ListBlocks.as_view(),          name='list_blocks'),
    url(r'^get_blocks_variation$',          handlers.GetBlockValidationVariation.as_view(),  name='get_blocks'),
    url(r'^get_blocks_gene$',               handlers.GetBlockValidationGene.as_view(),       name='get_blocks'),
    url(r'^get_blocks_disease$',            handlers.GetBlockValidationDisease.as_view(),    name='get_blocks'),
    url(r'^get_blocks_trait$',              handlers.GetBlockValidationTrait.as_view(),      name='get_blocks'),
    url(r'^get_blocks_treatment$',          handlers.GetBlockValidationTreatment.as_view(),  name='get_blocks'),
    url(r'^block_stable_update$',           handlers.BlockStableUpdate.as_view(),   name='block_stable_update'),
    url(r'^search$',                        handlers.Search.as_view(),              name='search'),
    url(r'^send_message_contact_us$',       handlers.SendMessageContactUs.as_view(),name='send_message_contact_us'),
    url(r'^get_lang_text$',                 handlers.GetLangText.as_view(),         name='get_lang_text'),
]
