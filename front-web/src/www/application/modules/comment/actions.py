from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from application.modules.common import page_contexts, actions as common_actions, components as common_components
from . import components

class LoadComment(common_actions.BaseAction):
    def POST(self):
        user = common_components.UserManager().parse_user(self.request);
        if user != False:
            self.params['username'] = user['username']
            self.params['idUser'] = user['userid']
        else:
            self.params['username'] = 'Anonymous'
        data = components.CommentStore(self.get_container()).load_comment(self.params)
        return JsonResponse(data)

class LikeComment(common_actions.BaseAction):
    def POST(self):
        user = common_components.UserManager().parse_user(self.request);
        if user != False:
            self.params['username'] = user['username']
            self.params['idUser'] = user['userid']
        else:
            self.params['username'] = 'Anonymous'
        data = components.CommentStore(self.get_container()).like_comment(self.params)
        return JsonResponse(data)

class DislikeComment(common_actions.BaseAction):
    def POST(self):
        user = common_components.UserManager().parse_user(self.request);
        if user != False:
            self.params['username'] = user['username']
            self.params['idUser'] = user['userid']
        else:
            self.params['username'] = 'Anonymous'
        data = components.CommentStore(self.get_container()).dislike_comment(self.params)
        return JsonResponse(data)

class ReplyComment(common_actions.BaseAction):
    def POST(self):
        user = common_components.UserManager().parse_user(self.request);
        if user != False:
            self.params['username'] = user['username']
            self.params['idUser'] = user['userid']
        else:
            self.params['username'] = 'Anonymous'
        data = components.CommentStore(self.get_container()).reply_comment(self.params)
        return JsonResponse(data)

class SubmitComment(common_actions.BaseAction):
    def POST(self):
        user = common_components.UserManager().parse_user(self.request);
        if user != False:
            self.params['username'] = user['username']
            self.params['idUser'] = user['userid']
        else:
            self.params['username'] = 'Anonymous'    
        data = components.CommentStore(self.get_container()).submit_comment(self.params)
        return JsonResponse(data)
