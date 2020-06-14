class LanguageMiddleware(object):
    def process_request(self, request):
        if 'lang' not in request.session:
            request.session['lang'] = 'en'
