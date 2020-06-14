
from django.conf.urls import include, url
from . import handlers

urlpatterns = [
    url(r'^get$',    handlers.Get.as_view(),      name='variation_get'),
    url(r'^view$',    handlers.View.as_view(),      name='variation_view'),
    url(r'^list$',   handlers.List.as_view(),     name='variation_list'),
    url(r'^create$',    handlers.Create.as_view(),      name='variation_create'),
    url(r'^update$',   handlers.Update.as_view(),     name='variation_update'),
    url(r'^delete$',    handlers.Delete.as_view(),      name='variation_delete'),
    url(r'^summary$',    handlers.Summary.as_view(),      name='variation_summary'),
    url(r'^get_genotype$',    handlers.GetGenotype.as_view(),      name='variation_get_genotype'),
    url(r'^get_eff_note$',    handlers.GetEffNote.as_view(),       name='variation_get_genotype')
]
