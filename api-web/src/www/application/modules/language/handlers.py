from notasquare.urad_api import *
from application.models import *
from application import constants

class List(handlers.standard.ListHandler):
    def create_query(self, data):
        query = Language.objects
        query = query.filter(is_disabled=False)
        if 'title' in data:
            query = query.filter(title__contains=data['title'])
        if 'code' in data:
            query = query.filter(code__contains=data['code'])
        return query
    def serialize_entry(self, data):
        return {
            'id':       data.id,
            'title':    data.title,
            'code':     data.code,
        }

class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        query = Language.objects.get(pk=data['id'])
        return {
            'id':       query.id,
            'title':    query.title,
            'code':     query.code
        }


class Create(handlers.standard.CreateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('title', 'string'):
            self.add_error('title', 'MUST_NOT_BE_EMPTY')
        if not parser.parse('code', 'string'):
            self.add_error('code', 'MUST_NOT_BE_EMPTY')
        return parser.get_data()
    def create(self, data):
        language = Language()
        language.title = data['title']
        language.code = data['code']
        language.save()

        return language

class Update(handlers.standard.UpdateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if 'title' in params:
            if not parser.parse('title', 'string'):
                self.add_error('title', 'MUST_NOT_BE_EMPTY')
        if 'code' in params:
            if not parser.parse('code', 'string'):
                self.add_error('code', 'MUST_NOT_BE_EMPTY')
        return parser.get_data()
    def update(self, data):
        language = Language.objects.get(pk=data['id'])
        if 'title' in data:
            language.title = data['title']
        if 'code' in data:
            language.code = data['code']
        language.save()

        return language


class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        language = Language.objects.get(pk=data['id'])
        language.is_disabled = True
        language.save()
        return 1
