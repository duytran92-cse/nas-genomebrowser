from django.conf import settings

class CommentStore(object):
    def __init__(self, container):
        self.container = container
    def load_comment(self, params):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/comment/load_comment', GET=params)
    def reply_comment(self, params):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/comment/reply_comment', POST=params)
    def like_comment(self, params):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/comment/like_comment', POST=params)
    def dislike_comment(self, params):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/comment/dislike_comment', POST=params)
    def submit_comment(self, params):
        return self.container.call_api(settings.GENOME_BROWSER_API_URL + '/comment/submit_comment', POST=params)
