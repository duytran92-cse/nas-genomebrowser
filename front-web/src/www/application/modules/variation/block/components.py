from django.conf import settings

class VariationBlockStore(object):
    def __init__(self, container):
        self.container = container
    def get(self, id):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/variation_block/get', GET={'id': id})
    def update(self, data, id):
        data['id'] = id
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/variation_block/update', POST=data)
    def save_text_eff(self, data):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/variation_block/save_text_eff', POST=data)
    def helper(self, id):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/variation_block/helper', GET={'id': id})
    def get_genotype(self, id):
        data = self.container.call_api(settings.GENOME_BROWSER_API_URL + '/variation/get_genotype', GET={'id': id})
        return data['data']
    def get_eff_note(self):
        data = self.container.call_api(settings.GENOME_BROWSER_API_URL + '/variation/get_eff_note', GET={})
        return data['data']
