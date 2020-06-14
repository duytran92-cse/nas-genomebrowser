from django.conf import settings

class PageStore(object):
    def __init__(self, container):
        self.container = container
    def get_content_page(self, id):
        data = self.container.call_api(settings.GENOME_BROWSER_API_URL + '/page/get_content_page', GET={'page_id': id})
        return data['data']
    def contact_us(self, params):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/page/send_message_contact_us', POST=params)
