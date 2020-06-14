from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.template import loader
from notasquare.urad_web import actions, page_contexts, widgets
from notasquare.urad_web_material import renderers
from notasquare.urad_web.renderers import BaseRenderer
from application import constants
from application.modules.common import helpers
from wsgiref.util import FileWrapper
import os, mimetypes, urllib


class Create(actions.crud.FormAction):
    def POST(self):
        upload_handler = helpers.CommonHelpers()
        upload_file = self.request.FILES['file']
        result = upload_handler.handle_uploaded_file(upload_file)
        return JsonResponse(result)


class Download(actions.crud.FormAction):
    def GET(self):
        mimetypes.init()
        original_filename = self.params['f']
        file_path = "{}/{}".format(settings.UPLOAD_ROOT, original_filename)
        if os.path.exists(file_path):
            fp = open(file_path, 'rb')
            response = HttpResponse(fp.read())
            fp.close()
            type, encoding = mimetypes.guess_type(original_filename)
            if type is None:
                type = 'application/octet-stream'
            response['Content-Type'] = type
            response['Content-Length'] = str(os.stat(file_path).st_size)
            if encoding is not None:
                response['Content-Encoding'] = encoding

            # To inspect details for the below code, see http://greenbytes.de/tech/tc2231/
            if u'WebKit' in self.request.META['HTTP_USER_AGENT']:
                # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
                filename_header = 'filename=%s' % original_filename.encode('utf-8')
            elif u'MSIE' in self.request.META['HTTP_USER_AGENT']:
                # IE does not support internationalized filename at all.
                # It can only recognize internationalized URL, so we do the trick via routing rules.
                filename_header = ''
            else:
                # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
                filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(original_filename.encode('utf-8'))
            response['Content-Disposition'] = 'attachment; ' + filename_header
            return response
        else:
            raise Http404