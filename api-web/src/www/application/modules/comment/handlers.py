from notasquare.urad_api import *
from application.models import *
from application import constants


class List(handlers.standard.ListHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        return parser.get_data()
    def create_query(self, data):
        query = Comment.objects
        query = query.filter(page=data['idPage'])
        if 'text' in data:
            query = query.filter(comment__contains=data['text'])
        return query
    def serialize_entry(self, page_comment):
        if page_comment.page == 'variation':
            page = Variation.objects.get(title=page_comment.entity)
        if page_comment.page == 'gene':
            page = Gene.objects.get(title=page_comment.entity)
        if page_comment.page == 'disease':
            page = Disease.objects.get(title=page_comment.entity)
        if page_comment.page == 'trait':
            page = Trait.objects.get(title=page_comment.entity)
        if page_comment.page == 'treatment':
            page = Treatment.objects.get(title=page_comment.entity)
        user = User.objects.get(pk=page_comment.user_id)
        return {
            'id': page_comment.id,
            'page': page_comment.page,
            'comment': page_comment.comment,
            'timestamp': page_comment.timestamp,
            'root': page_comment.root,
            'numLike': page_comment.numLike,
            'entity': page_comment.entity,
            'user': user.name,
            'page_id': page.id
        }


class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        comment = Comment.objects.get(pk=data['id'])
        user = User.objects.get(pk=comment.user_id)

        return {
            'id':           comment.id,
            'timestamp':    comment.timestamp,
            'comment':      comment.comment,
            'user':         user.name
        }


class Create(handlers.standard.CreateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('comment', 'string'):
            self.add_error('comment', 'MUST_NOT_BE_EMPTY')
        return parser.get_data()
    def create(self, data):
        page_comment = Comment()
        page_comment.page = data['page']
        # Check exist user
        try:
            user = User.objects.get(name=data['username'])
        except User.DoesNotExist:
            user = User()
            user.name = data['username']
            user.save()
        # Get entity name
        if data['page'] == 'variation':
            entity = Variation.objects.get(pk=data['entity'])
        elif data['page'] == 'disease':
            entity = Disease.objects.get(pk=data['entity'])
        if data['page'] == 'gene':
            entity = Gene.objects.get(pk=data['entity'])
        if data['page'] == 'trait':
            entity = Trait.objects.get(pk=data['entity'])
        if data['page'] == 'treatment':
            entity = Treatment.objects.get(pk=data['entity'])

        page_comment.user_id = user.id
        page_comment.comment = data['comment']
        page_comment.entity = entity.title
        page_comment.save()
        return page_comment


class Update(handlers.standard.UpdateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('id', 'integer'):
            self.add_error('id', 'MUST_NOT_BE_EMPTY')
        if 'comment' in params:
            if not parser.parse('comment', 'string'):
                self.add_error('comment', 'MUST_NOT_BE_EMPTY')
        return parser.get_data()
    def update(self, data):
        # Only update comment field
        page_comment = Comment.objects.get(pk=data['id'])
        if 'comment' in data:
            page_comment.comment = data['comment']
        page_comment.save()
        return page_comment


class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        page_comment = Comment.objects.get(pk=data['id'])
        page_comment.delete()
        return 1

# Comment actions
class LoadComment(handlers.standard.GetHandler):
    def get_data(self, data):
        entities = Comment.objects.filter(page=data['idPage'], entity=data['entity'], root=0).order_by('-timestamp')
        comments = []
        if entities:
            for comment in entities:
                commentUserLike = CommentUserLike.objects.filter(comment_id=comment.id)
                if commentUserLike:
                    commentUserLike = commentUserLike.count()
                else:
                    commentUserLike = 0
                replies = []
                replyEntity = Comment.objects.filter(root=comment.id)
                if replyEntity:
                    for reply in replyEntity:
                        commentUserLikeReply = CommentUserLike.objects.filter(comment_id=reply.id)
                        if commentUserLikeReply:
                            commentUserLikeReply = commentUserLikeReply.count()
                        else:
                            commentUserLikeReply = 0
                        user = User.objects.get(pk=reply.user_id)

                        replies.append({
                            'id': reply.id,
                            'root': reply.root,
                            'content': reply.comment,
                            'numLike': commentUserLikeReply,
                            'createdAt': reply.timestamp,
                            'userName': user.name
                        })
                user = User.objects.get(pk=comment.user_id)

                comments.append({
                    'id': comment.id,
                    'root': comment.id,
                    'content': comment.comment,
                    'numLike': commentUserLike,
                    'numReply': len(replies),
                    'replies': replies,
                    'createdAt': comment.timestamp,
                    'userName': user.name
                })
        data = {
            'comments': comments,
            'currentUser': 'Anonymous'
        }
        return data

class SubmitComment(handlers.standard.FormHandler):
    def POST(self, data):
        page_comment = Comment()
        page_comment.page = data['idPage']
        if 'timestamp' in data:
            page_comment.timestamp = data['timestamp']
        # page_comment.user_id = data['user']
        try:
            user = User.objects.get(name=data['username'])
        except User.DoesNotExist:
            user = User()
            user.name = data['username']
            user.save()

        page_comment.user_id = user.id # Fix me
        page_comment.comment = data['content']
        page_comment.entity = data['entity']
        page_comment.root = 0
        page_comment.save()
        return ('200', '')

class ReplyComment(handlers.standard.FormHandler):
    def POST(self, data):
        page_comment = Comment()
        page_comment.page = data['idPage']
        if 'timestamp' in data:
            page_comment.timestamp = data['timestamp']
        try:
            user = User.objects.get(name=data['username'])
        except User.DoesNotExist:
            user = User()
            user.name = data['username']
            user.save()

        page_comment.user_id = user.id
        page_comment.comment = data['content']
        page_comment.entity = data['entity']
        page_comment.root = data['root']
        page_comment.save()
        return ('200', '')

class LikeComment(handlers.standard.FormHandler):
    def POST(self, data):
        comment = CommentUserLike.objects.filter(comment_id=data['idComment'], user_id=data['idUser'])
        if comment:
            pass
        else:
            page_comment = CommentUserLike()
            page_comment.user_id=data['idUser']
            page_comment.comment_id=data['idComment']
            page_comment.save()
        return ('200', '')

class DislikeComment(handlers.standard.FormHandler):
    def POST(self, data):
        comment = CommentUserLike.objects.filter(comment_id=data['idComment'], user_id=data['idUser'])
        if comment:
            comment.delete()
        return ('200', '')
