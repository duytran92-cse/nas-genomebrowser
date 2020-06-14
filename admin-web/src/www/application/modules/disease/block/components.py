from django.conf import settings
from application.modules.common import page_contexts

class DiseaseBlockStore(object):
    def __init__(self, container):
        self.container = container
    def list(self, params={}, sortkey='id', sortdir='desc', page_number=1):
        params['_pager_start'] = (page_number - 1) * 10
        params['_pager_num'] = 10
        params['_sort_key'] = sortkey
        params['_sort_dir'] = sortdir
        data = self.container.call_api(settings.GENOME_BROWSER_API_URL + '/disease_block/list', GET=params)
        return data['data']
    def get(self, id):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/disease_block/get', GET={'id': id})
    def create(self, data):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/disease_block/create', POST=data)
    def update(self, data, id):
        data['id'] = id
        data['verify'] = True
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/disease_block/update', POST=data)
    def delete(self, id):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/disease_block/delete', POST={'id': id})
