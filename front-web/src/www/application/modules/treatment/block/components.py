from django.conf import settings

class TreatmentBlockStore(object):
    def __init__(self, container):
        self.container = container
    def get(self, id):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/treatment_block/get', GET={'id': id})
    def update(self, data, id):
        data['id'] = id
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/treatment_block/update', POST=data)
    def helper(self, id):
       return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/treatment_block/helper', GET={'id': id}) 
