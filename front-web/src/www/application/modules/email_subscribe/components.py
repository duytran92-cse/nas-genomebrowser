from django.conf import settings

class EmailSubcribeStore(object):
    def __init__(self, container):
        self.container = container
    def email_subscribe(self, data):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/email_subscribe/create', POST=data)
