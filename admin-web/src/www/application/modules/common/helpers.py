from django.conf import settings
import os
class CommonHelpers(object):
   def handle_uploaded_file(self, f):
       path = "{}/{}".format(settings.UPLOAD_ROOT, f.name)
       if not os.path.exists(os.path.dirname(path)):
           os.makedirs(os.path.dirname(path))
       path = "{}/{}".format(settings.UPLOAD_ROOT, f.name)
       with open(path, 'wb+') as destination:
           for chunk in f.chunks():
               destination.write(chunk)
       return {'url': '/file_upload/download?f={}'.format(f.name), 'name': f.name}
