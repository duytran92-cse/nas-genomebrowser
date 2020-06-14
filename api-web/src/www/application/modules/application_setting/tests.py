import json
from django.utils.module_loading import import_string
from notasquare.urad_api import tests
from application.models import *


class UnitTest(tests.BaseUnitTest):
    def setUp(self):
        Page.objects.create(kind='page', title='Page Title')
    def test_basic(self):
        self.init()
        self.set_headers({
            'NAS-TEST-USER-ID':       1,
            'NAS-TEST-USER-USERNAME': 'vaquan'
        })
        self.get('GET application setting', '/application_setting/get')
        self.post('Update application setting', '/application_setting/update', {
            'application_title':       'Application Title',
            'contact_address_text':    'Contact Address Text',
            'about_genopedia_text':    'About Genopedia Text',
            'facebook_url':            'Facebook URL',
            'twitter_url':             'Twitter URL',
            'youtube_url':             'Youtube URL',
            'linkedin_url':            'LinkedIn URL',
            'google_plus_url':         'Google+ URL',
            'copyright_page_id':       1,
            'impression_page_id':      1,
            'privacy_page_id':         1,
            'term_of_use_page_id':     1,
            'stat_num_variation':                 10,
            'stat_num_gene':                      11,
            'stat_num_disease':                   12,
            'stat_num_disease_causing_mutation':  13,
            'stat_num_trait':                     14,
            'stat_num_drug':                      15,
            'stat_num_treatment':                 16,
            'stat_num_cited_publication':         17,
            'stat_num_page':                      18,
            'stat_num_registered_user':           19,
            'stat_num_genetic_code_letter':       20,
            'stat_num_forum_post':                21,
        })
        self.get('GET application setting', '/application_setting/get')
