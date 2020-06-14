from django.conf import settings

class GeneStore(object):
    def __init__(self, container):
        self.container = container
    def list(self, params={}, sortkey='title', sortdir='asc', page_number=1, letter='a'):
        params['_pager_start'] = (page_number - 1) * 30
        params['_pager_num'] = 60
        params['_sort_key'] = sortkey
        params['_sort_dir'] = sortdir
        params['letter'] = letter
        data = self.container.call_api(settings.GENOME_BROWSER_API_URL + '/gene/list', GET=params)
        return data['data']
    def get(self, id):
       return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/gene/view', GET={'id': id})
