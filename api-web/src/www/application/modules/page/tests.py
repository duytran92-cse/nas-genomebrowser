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
            'NAS-TEST-USER-USERNAME': 'vaquan'
        })
        self.get ('List all page', '/page/list')
        self.post('Create new page', '/page/create', {
            'kind':      'variation',
            'title':     'rs12345'
        })
        self.post('Create new page (empty)', '/page/create', {
        })
        self.post('Create new page (empty 2)', '/page/create', {
            'kind':      '',
            'title':     ''
        })
        self.get('GET page id=1', '/page/get?id=1')
        self.get ('List all pages', '/page/list')
        self.post('Update page id=1', '/page/update', {
            'id':        1,
            'kind':      'variation',
            'title':     'rs1234556666666'
        })
        self.get ('List all pages', '/page/list')
        self.post('Delete page id=1', '/page/delete', {
            'id':        1
        })
        self.get ('List all variables', '/page/list')
