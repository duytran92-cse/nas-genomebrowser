from django.conf import settings

class TraitBlockStore(object):
    def __init__(self, container):
        self.container = container
    def get(self, id):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/trait_block/get', GET={'id': id})
    def update(self, data, id):
        data['id'] = id
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/trait_block/update', POST=data)
    def helper(self, id):
       return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/trait_block/helper', GET={'id': id})
