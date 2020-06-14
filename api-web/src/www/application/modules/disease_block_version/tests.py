import json
from django.utils.module_loading import import_string
from notasquare.urad_api import tests
from application.models import *


class UnitTest(tests.BaseUnitTest):
    def setUp(self):
        Page.objects.create(kind='variation', title="rs123")
    def test_basic(self):
        self.init()
        self.set_headers({
            'NAS-TEST-USER-ID':       1,
            'NAS-TEST-USER-USERNAME': 'vaquan'
        })
        self.get ('List all page block', '/page_block/list?page_id=1')
        self.post('Create new page block', '/page_block/create', {
            'page_id':       1,
            'kind':          'general_text',
            'position':      'main',
            'title':         'Block title',
            'sort_order':    1
        })
        self.post('Create new page block (empty)', '/page_block/create', {
        })
        self.post('Create new page block (empty 2)', '/page_block/create', {
            'page_id':       0,
            'kind':          '',
            'position':      '',
            'title':         '',
            'sort_order':    0
        })
        self.get('GET page block id=1', '/page_block/get?id=1')
        self.get ('List all page blocks', '/page_block/list?page_id=1')
        self.post('Update page block id=1', '/page_block/update', {
            'id':            1,
            'kind':          'general_text',
            'position':      'left',
            'title':         'Block title (*)',
            'text':          'This is blah blah',
            'sort_order':    2
        })
        self.get ('List all page blocks', '/page_block/list?page_id=1')
        self.post('Delete page block id=1', '/page_block/delete', {
            'id':            1
        })
        self.get ('List all page blocks', '/page_block/list?page_id=1')
