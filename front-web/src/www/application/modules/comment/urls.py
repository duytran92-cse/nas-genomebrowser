
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^load_comment$',    actions.LoadComment.as_view(),      name='load_comment'),
    url(r'^reply_comment$',   actions.ReplyComment.as_view(),     name='reply_comment'),
    url(r'^like_comment$', actions.LikeComment.as_view(),   name='like_comment'),
    url(r'^dislike_comment$', actions.DislikeComment.as_view(),   name='dislike_comment'),
    url(r'^submit_comment$', actions.SubmitComment.as_view(),   name='submit_comment'),
]
