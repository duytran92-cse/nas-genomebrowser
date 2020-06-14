from django.conf import settings
import jwt
class ApplicationSettingStore(object):
    def __init__(self, container):
        self.container = container
    def get(self):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/application_setting/get', GET={})


class PageStore(object):
    def __init__(self, container):
        self.container = container
    def get(self, id):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/page/get', GET={'id': id})
    def get_lang_text(self, lang):
        data = self.container.call_api(settings.GENOME_BROWSER_API_URL + '/page/get_lang_text', GET={'lang': lang})
        return data['data']

class UserManager(object):
    def __init__(self):
        pass
    def parse_user(self,request):
        encoded = request.COOKIES.get('_gpfront_jwt')
        if encoded:
            user = jwt.decode(encoded, settings.OAUTH_CLIENT_EK, algorithms=['HS256'])
            if 'userid' in user:
                return user
        return False
