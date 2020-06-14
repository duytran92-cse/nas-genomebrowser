from notasquare.urad_api import *
from application.models import *
from application import constants
import re

class List(handlers.standard.ListHandler):
    def create_query(self, data):
        query = EmailSubscribe.objects
        if 'email' in data:
            query = query.filter(email__contains=data['email'])
        return query
    def serialize_entry(self, data):
        return {
            'id':       data.id,
            'email':     data.email,
        }

class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        query = EmailSubscribe.objects.get(pk=data['id'])
        return {
            'id':           query.id,
            'email':         query.email,
        }


class Create(handlers.standard.CreateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('email', 'string'):
            self.add_error('text', 'MUST_NOT_BE_EMPTY')
        return parser.get_data()
    def create(self, data):
        email_subscribe = EmailSubscribe()
        email_subscribe.email = data['email']
        email_subscribe.save()
        return email_subscribe

class Update(handlers.standard.UpdateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('email', 'string'):
            self.add_error('text', 'MUST_NOT_BE_EMPTY')
        return parser.get_data()
    def update(self, data):
        email_subscribe = EmailSubscribe.objects.get(pk=data['id'])
        email_subscribe.email = data['email']
        email_subscribe.save()
        return email_subscribe


class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        EmailSubscribe.objects.get(pk=data['id']).delete()
        return 1
