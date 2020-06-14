from django.conf.urls import include, url

urlpatterns = [
    url(r'^',                               include('application.modules.dashboard.urls')),
    url(r'^dashboard',                      include('application.modules.dashboard.urls')),
    url(r'^email_subscribe/',                include('application.modules.email_subscribe.urls')),
    url(r'^variation/',                     include('application.modules.variation.urls')),
    url(r'^disease/',                       include('application.modules.disease.urls')),
    url(r'^gene/',                          include('application.modules.gene.urls')),
    url(r'^trait/',                         include('application.modules.trait.urls')),
    url(r'^treatment/',                     include('application.modules.treatment.urls')),
    url(r'^page/',                          include('application.modules.page.urls')),
    url(r'^application_setting/',           include('application.modules.application_setting.urls')),
    url(r'^file_upload/',                   include('application.modules.file_upload.urls')),
    url(r'^text_block/',                    include('application.modules.application_setting.text_block.urls')),
    url(r'^language/',                      include('application.modules.application_setting.language.urls')),
]
