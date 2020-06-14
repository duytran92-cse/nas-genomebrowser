"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from application.modules.home import actions

urlpatterns = [
    url(r'^variation/',             include('application.modules.variation.urls')),
    url(r'^gene/',                  include('application.modules.gene.urls')),
    url(r'^disease/',               include('application.modules.disease.urls')),
    url(r'^trait/',                 include('application.modules.trait.urls')),
    url(r'^treatment/',             include('application.modules.treatment.urls')),
    url(r'^',                       include('application.modules.home.urls')),
    url(r'^variation_block/',       include('application.modules.variation.block.urls')),
    url(r'^gene_block/',            include('application.modules.gene.block.urls')),
    url(r'^disease_block/',         include('application.modules.disease.block.urls')),
    url(r'^trait_block/',           include('application.modules.trait.block.urls')),
    url(r'^treatment_block/',       include('application.modules.treatment.block.urls')),
    url(r'^comment/',               include('application.modules.comment.urls')),
    url(r'^email_subscribe$',       include('application.modules.email_subscribe.urls')),
    url(r'^search',                 include('application.modules.search.urls')),
    url(r'^impression$',            actions.Impression.as_view(),       name='impression'),
    url(r'^term-of-use$',           actions.TermOfUse.as_view(),        name='term_of_use'),
    url(r'^privacy$',               actions.Privacy.as_view(),          name='privacy'),
    url(r'^copyright$',             actions.Copyright.as_view(),        name='copyright'),
    url(r'^send_message_contact_us$',actions.SendMessageContactUs.as_view(), name='send_message_contact_us'),

    url(r'^change_language$',       actions.ChangeLanguage.as_view(),   name='change_language'),
]
