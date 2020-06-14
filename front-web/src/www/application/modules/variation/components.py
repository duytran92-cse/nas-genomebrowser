from django.conf import settings

class VariationStore(object):
    def __init__(self, container):
        self.container = container
    def list(self, params={}, sortkey='title', sortdir='asc', page_number=1):
        params['_pager_start'] = (page_number - 1) * 30
        params['_pager_num'] = 60
        params['_sort_key'] = sortkey
        params['_sort_dir'] = sortdir
        if 'user_id' in params:
            var = self.container.call_api(settings.GENOPEDIA_USER_API_URL + '/user-variation/list', GET={'user_id': params['user_id']})
            variation = []
            if len(var['data']['records']) > 0:
                for i in var['data']['records']:
                    variation.append(i['rsnumber'])
            if len(variation) > 0:
                params['rs_filter'] = variation
        data = self.container.call_api(settings.GENOME_BROWSER_API_URL + '/variation/list', GET=params)
        return data['data']
    def get(self, params):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/variation/view', GET={'id': params['rsnumber'], 'filter': params['filter']})
