from django.conf import settings

class SearchStore(object):
    def __init__(self, container):
        self.container = container
    def search(self, params):
        data = self.container.call_api(settings.GENOME_BROWSER_API_URL + '/page/search', GET={'kw': params})
        return data['data']['record']
