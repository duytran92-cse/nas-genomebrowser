import json
from django.utils.module_loading import import_string
from notasquare.urad_api import tests
from application.models import *


class UnitTest(tests.BaseUnitTest):
    def setUp(self):
        pass

    def test_basic(self):
        self.init()
        self.set_headers({
            'NAS-TEST-USER-ID':       1,
            'NAS-TEST-USER-USERNAME': 'tdquang'
        })
        self.post('Create new page', '/page/create', {
            'kind':      'variation',
            'title':     'rs2'
        })
        self.get ('List all variations', '/variation/list')        
        self.get('GET variation id=1', '/variation/get?id=1') 