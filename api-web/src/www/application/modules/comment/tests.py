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
        self.get ('List all page comment', '/page_comment/list?page_id=1')
        self.post('Create new page comment', '/page_comment/create', {
            'page_id':       1,
            'timestamp':     '2016-12-22 01:01:01',
            'user':          'vaquan',
            'comment':       'Hello World, this is a comment'
        })
        self.post('Create new page comment (empty)', '/page_comment/create', {
        })
        self.post('Create new page comment (empty 2)', '/page_comment/create', {
            'page_id':       0,
            'timestamp':     '',
            'user':          '',
            'comment':       ''
        })
        self.get('GET page comment id=1', '/page_comment/get?id=1')
        self.get ('List all page comments', '/page_comment/list?page_id=1')
        self.post('Update page comment id=1', '/page_comment/update', {
            'id':            1,
            'timestamp':     '2015-05-05 05:05:05',
            'user':          'abc',
            'comment':       'Hehe'
        })
        self.get ('List all page comments', '/page_comment/list?page_id=1')
        self.post('Delete page block id=1', '/page_comment/delete', {
            'id':            1
        })
        self.get ('List all page blocks', '/page_comment/list?page_id=1')
