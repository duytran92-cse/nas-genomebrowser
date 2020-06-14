from notasquare.urad_api import *
from application.models import *
from application import constants
import re

class List(handlers.standard.ListHandler):
    def create_query(self, data):
        query = TextBlock.objects
        query = query.filter(is_disabled=False)
        if 'text' in data:
            query = query.filter(text__contains=data['text'])
        return query
    def serialize_entry(self, data):
        return {
            'id':       data.id,
            'text':     data.text,
            'kind':     data.kind
        }

class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        query = TextBlock.objects.get(pk=data['id'])
        text_lang = TextBlockLanguage.objects.filter(text_block_id=query.id)
        translation = []
        for item in text_lang:
            translation.append({
                'language':         item.language,
                'translate':        item.translate
            })
        return {
            'id':           query.id,
            'text':         query.text,
            'kind':         query.kind,
            'text_code':    query.text_code,
            'translation':  translation
        }


class Create(handlers.standard.CreateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('text', 'string'):
            self.add_error('text', 'MUST_NOT_BE_EMPTY')
        if not parser.parse('kind', 'string'):
            self.add_error('kind', 'MUST_NOT_BE_EMPTY')
        return parser.get_data()
    def create(self, data):
        text_block = TextBlock()
        text_block.text = data['text']
        text_block.kind = data['kind']
        # Remove special character in text string
        spe_str = re.sub('[^a-zA-Z0-9-_* .]', '', data['text'])
        # Convert text string to lowercase
        spe_str = spe_str.lower()
        # Convert text string to text_string
        text_code = spe_str.replace(' ', '_')
        text_block.text_code = text_code
        text_block.save()
        for item in data['translation']:
            text_lang = TextBlockLanguage()
            text_lang.text_block_id = text_block.id
            text_lang.language = item['language']
            text_lang.translate = item['translate']
            text_lang.save()
        return text_block

class Update(handlers.standard.UpdateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        return parser.get_data()
    def update(self, data):
        text_block = TextBlock.objects.get(pk=data['id'])
        TextBlockLanguage.objects.filter(text_block_id=data['id']).delete()
        for item in data['translation']:
            text_lang = TextBlockLanguage()
            text_lang.text_block_id = text_block.id
            text_lang.language = item['language']
            text_lang.translate = item['translate']
            text_lang.save()
        return text_block


class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        text_block = TextBlock.objects.get(pk=data['id'])
        text_block.is_disabled = True
        text_block.save()
        return 1
