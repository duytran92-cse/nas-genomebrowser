
from django.conf.urls import include, url
from . import handlers

urlpatterns = [
    url(r'^get$',    handlers.Get.as_view(),      name='comment_get'),
    url(r'^list$',   handlers.List.as_view(),     name='comment_list'),
    url(r'^create$', handlers.Create.as_view(),   name='comment_create'),
    url(r'^update$', handlers.Update.as_view(),   name='comment_update'),
    url(r'^delete$', handlers.Delete.as_view(),   name='comment_delete'),
    url(r'^load_comment$',    handlers.LoadComment.as_view(),      name='load_comment'),
    url(r'^reply_comment$',   handlers.ReplyComment.as_view(),     name='reply_comment'),
    url(r'^like_comment$', handlers.LikeComment.as_view(),   name='like_comment'),
    url(r'^dislike_comment$', handlers.DislikeComment.as_view(),   name='dislike_comment'),
    url(r'^submit_comment$', handlers.SubmitComment.as_view(),   name='submit_comment'),
]
