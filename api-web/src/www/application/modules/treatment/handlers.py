from notasquare.urad_api import *
from application.models import *
from application import constants
from application.modules.treatment_block import components as block_components

class List(handlers.standard.ListHandler):
    def create_query(self, data):
        query = Treatment.objects
        query = query.filter(is_disabled=False)
        if 'text' in data:
            query = query.filter(title__contains=data['text'])
        if 'letter' in data:
            if data['letter'] != 'all':
                query = query.filter(title__istartswith=data['letter'])
        return query
    def serialize_entry(self, data):
        return {
            'id':       data.id,
            'title':    data.title
        }

class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        result = {}
        treatment = Treatment.objects.get(pk=data['id'])
        result['id']      = treatment.id
        result['title']   = treatment.title

        return result

class View(handlers.standard.GetHandler):
    def get_data(self, data):
        result = {}
        block_helper = block_components.TreatmentBlockHelper()
        treatment = Treatment.objects.get(title=data['id'])
        blocks = { 'main': [], 'left': [],'right': []}
        rows = TreatmentBlock.objects.filter(treatment_id=treatment.id, is_disabled = False).order_by('sort_order').all()
        for r in rows:
            block = block_helper.load_treatment_block(r.id)
            blocks[r.position].append(block)
        result['id']      = treatment.id
        result['title']   = treatment.title
        result['blocks']  = blocks
        return result

class Create(handlers.standard.CreateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if not parser.parse('title', 'string'):
            self.add_error('title', 'MUST_NOT_BE_EMPTY')
        return parser.get_data()
    def create(self, data):
        treatment = Treatment()
        treatment.title = data['title']
        treatment.save()
        return treatment

class Update(handlers.standard.UpdateHandler):
    def parse_and_validate(self, params):
        parser = self.container.create_parser(params)
        if 'title' in params:
            if not parser.parse('title', 'string'):
                self.add_error('title', 'MUST_NOT_BE_EMPTY')
        return parser.get_data()
    def update(self, data):
        treatment = Treatment.objects.get(pk=data['id'])
        if 'title' in data:
            treatment.title = data['title']
        treatment.save()
        return treatment


class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        treatment = Treatment.objects.get(pk=data['id'])
        treatment.is_disabled = True
        treatment.save()
        return 1

class Summary(handlers.standard.GetHandler):
    def get_data(self, data):
        result = []
        blocks = []
        comments = []
        active_blocks_version = []
        inactive_blocks_version = []

        treatment = Treatment.objects.get(pk=data['treatment_id'])

        treatment_blocks = TreatmentBlock.objects.filter(treatment_id=data['treatment_id'],is_disabled=False)[:5]
        for item in treatment_blocks:

            # Get active and latest version
            if item.kind == 'general_text':
                query = TreatmentBlockVersion.objects.filter(treatment_block_id=item.id, version_status='active', is_disabled=False)
            elif item.kind == 'general_alias':
                query = TreatmentBlockAliasVersion.objects.filter(treatment_block_id=item.id, version_status='active', is_disabled=False)
            elif item.kind == 'general_publications':
                query = TreatmentBlockPublicationVersion.objects.filter(treatment_block_id=item.id, version_status='active', is_disabled=False)

            active_version = query.filter(is_stable=True).order_by('-created_at')[:1]
            latest_version = query.order_by('-created_at')[:1]
            l_ver = 0
            ac_ver = 0
            if latest_version.first():
                l_ver = latest_version.first().version

            if active_version.first():
                ac_ver = active_version.first().version

            blocks.append({
                'id': item.id,
                'kind': item.kind,
                'position': item.position,
                'title': item.title,
                'text': item.text,
                'sort_order': item.sort_order,
                'page_id': item.treatment_id,
                'active_version': ac_ver,
                'latest_version': l_ver
            })
        total_blocks = TreatmentBlock.objects.filter(treatment_id=data['treatment_id'],is_disabled=False).count()

        active_blocks_versions = TreatmentBlockVersion.objects.filter(treatment_id=data['treatment_id'],is_disabled=False, version_status='active')[:5]
        for item in active_blocks_versions:
            block = TreatmentBlock.objects.get(pk=item.treatment_block_id)
            active_blocks_version.append({
                'id': item.id,
                'title': item.title,
                'text': item.text,
                'author': item.author,
                'version': item.version,
                'page_id': item.treatment_id,
                'page_block_id': item.treatment_block_id,
                'kind': block.kind,
                'timestamp': item.created_at
            })
        total_active_blocks_version = TreatmentBlockVersion.objects.filter(treatment_id=data['treatment_id'],is_disabled=False, version_status='active').count()

        inactive_blocks_versions = TreatmentBlockVersion.objects.filter(treatment_id=data['treatment_id'],is_disabled=False, version_status='inactive')[:10]
        for item in inactive_blocks_versions:
            block = TreatmentBlock.objects.get(pk=item.treatment_block_id)
            inactive_blocks_version.append({
                'id': item.id,
                'title': item.title,
                'text': item.text,
                'author': item.author,
                'version': item.version,
                'page_id': item.treatment_id,
                'page_block_id': item.treatment_block_id,
                'kind': block.kind,
                'timestamp': item.created_at
            })
        total_inactive_blocks_version = TreatmentBlockVersion.objects.filter(treatment_id=data['treatment_id'],is_disabled=False, version_status='inactive').count()

        treatment_comment = Comment.objects.filter(page='treatment',entity=treatment.title)[:5]

        for item in treatment_comment:
            user = User.objects.get(pk=item.user_id)
            comments.append({
                'id': item.id,
                'timestamp': item.timestamp,
                'user': user.name,
                'comment': item.comment,
                'page_id': data['treatment_id']
            })
        total_comments = Comment.objects.filter(page='treatment',entity=treatment.title).count()

        result.append({
            'treatment_id': data['treatment_id'],
            'title': treatment.title,
            'blocks': blocks,
            'total_blocks': total_blocks,
            'total_active_blocks_version': total_active_blocks_version,
            'active_blocks_version': active_blocks_version,
            'total_inactive_blocks_version': total_inactive_blocks_version,
            'inactive_blocks_version': inactive_blocks_version,
            'total_comments': total_comments,
            'comments': comments
        })

        return (result)
