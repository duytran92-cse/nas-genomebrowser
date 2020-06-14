from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.template import loader
from notasquare.urad_web import actions, widgets, renderers
from application.themes.genopedia import renderers as genopedia_renderers
from application.modules.common import page_contexts, actions as common_actions, components as common_components
from application import constants
from . import components

class Home(common_actions.BaseAction):
    class StatisticsWidget(widgets.BaseWidget):
        def __init__(self):
            self.num_variation = 0
            self.num_gene = 0
            self.num_disease = 0
            self.num_disease_causing_mutation = 0
            self.num_trait = 0
            self.num_drug = 0
            self.num_treatment = 0
            self.num_cited_publication = 0
            self.num_page = 0
            self.num_registered_user = 0
            self.num_genetic_code_letter = 0
            self.num_forum_post = 0
    class StatisticsWidgetRenderer(renderers.BaseRenderer):
        def render(self, statistics_widget):
            template = loader.get_template('genopedia/home/statistics.html')
            context = {}
            context['num_variation'] = statistics_widget.num_variation
            context['num_gene'] = statistics_widget.num_gene
            context['num_disease'] = statistics_widget.num_disease
            context['num_disease_causing_mutation'] = statistics_widget.num_disease_causing_mutation
            context['num_trait'] = statistics_widget.num_trait
            context['num_drug'] = statistics_widget.num_drug
            context['num_treatment'] = statistics_widget.num_treatment
            context['num_cited_publication'] = statistics_widget.num_cited_publication
            context['num_page'] = statistics_widget.num_page
            context['num_registered_user'] = statistics_widget.num_registered_user
            context['num_genetic_code_letter'] = statistics_widget.num_genetic_code_letter
            context['num_forum_post'] = statistics_widget.num_forum_post
            return template.render(context)
    def create_statistics_widget(self):
        statistics_widget = self.StatisticsWidget()
        statistics_widget.renderer = self.StatisticsWidgetRenderer()

        record = common_components.ApplicationSettingStore(self.get_container()).get()
        application_setting = record['data']['record']
        statistics_widget.num_variation = application_setting['stat_num_variation']
        statistics_widget.num_gene = application_setting['stat_num_gene']
        statistics_widget.num_disease = application_setting['stat_num_disease']
        statistics_widget.num_disease_causing_mutation = application_setting['stat_num_disease_causing_mutation']
        statistics_widget.num_trait = application_setting['stat_num_trait']
        statistics_widget.num_drug = application_setting['stat_num_drug']
        statistics_widget.num_treatment = application_setting['stat_num_treatment']
        statistics_widget.num_cited_publication = application_setting['stat_num_cited_publication']
        statistics_widget.num_page = application_setting['stat_num_page']
        statistics_widget.num_registered_user = application_setting['stat_num_registered_user']
        statistics_widget.num_genetic_code_letter = application_setting['stat_num_genetic_code_letter']
        statistics_widget.num_forum_post = application_setting['stat_num_forum_post']

        return statistics_widget
    def GET(self):
        page_context = self.create_page_context()
        statistics_widget = self.create_statistics_widget()
        page_context.add_widget(statistics_widget)
        return HttpResponse(page_context.render())

class Impression(common_actions.BaseAction):
    class ImpressionRenderer(renderers.BaseRenderer):
        def render(self, table):
            template = loader.get_template('genopedia/page/impression.html')
            context = {}
            context['impression'] = table.data['content']
            return template.render(context)
    def create_table(self):
        table = widgets.table.DataTable()
        table.renderer = self.ImpressionRenderer()
        return table
    def load_table_data(self):
        record = common_components.ApplicationSettingStore(self.get_container()).get()
        application_setting = record['data']['record']
        page_id = application_setting['impression_page']
        return components.PageStore(self.get_container()).get_content_page(page_id)
    def GET(self):
        page_context = self.create_page_context()
        table_widget = self.create_table()
        data = self.load_table_data()
        data = data['record']
        table_widget.set_data(data)
        page_context.add_widget(table_widget)
        return HttpResponse(page_context.render())

class TermOfUse(common_actions.BaseAction):
    class TermOfUseRenderer(renderers.BaseRenderer):
        def render(self, table):
            template = loader.get_template('genopedia/page/term_conditions.html')
            context = {}
            context['termConditions'] = table.data['content']
            return template.render(context)
    def create_table(self):
        table = widgets.table.DataTable()
        table.renderer = self.TermOfUseRenderer()
        return table
    def load_table_data(self):
        record = common_components.ApplicationSettingStore(self.get_container()).get()
        application_setting = record['data']['record']
        page_id = application_setting['term_of_use_page']
        return components.PageStore(self.get_container()).get_content_page(page_id)
    def GET(self):
        page_context = self.create_page_context()
        table_widget = self.create_table()
        data = self.load_table_data()
        data = data['record']
        table_widget.set_data(data)
        page_context.add_widget(table_widget)
        return HttpResponse(page_context.render())

class Privacy(common_actions.BaseAction):
    class PrivacyRenderer(renderers.BaseRenderer):
        def render(self, table):
            template = loader.get_template('genopedia/page/privacy.html')
            context = {}
            context['privacy'] = table.data['content']
            return template.render(context)
    def create_table(self):
        table = widgets.table.DataTable()
        table.renderer = self.PrivacyRenderer()
        return table
    def load_table_data(self):
        record = common_components.ApplicationSettingStore(self.get_container()).get()
        application_setting = record['data']['record']
        page_id = application_setting['privacy_page']
        return components.PageStore(self.get_container()).get_content_page(page_id)
    def GET(self):
        page_context = self.create_page_context()
        table_widget = self.create_table()
        data = self.load_table_data()
        data = data['record']
        table_widget.set_data(data)
        page_context.add_widget(table_widget)
        return HttpResponse(page_context.render())

class Copyright(common_actions.BaseAction):
    class CopyrightRenderer(renderers.BaseRenderer):
        def render(self, table):
            template = loader.get_template('genopedia/page/copyright.html')
            context = {}
            context['copyright'] = table.data['content']
            return template.render(context)
    def create_table(self):
        table = widgets.table.DataTable()
        table.renderer = self.CopyrightRenderer()
        return table
    def load_table_data(self):
        record = common_components.ApplicationSettingStore(self.get_container()).get()
        application_setting = record['data']['record']
        page_id = application_setting['copyright_page']
        return components.PageStore(self.get_container()).get_content_page(page_id)
    def GET(self):
        page_context = self.create_page_context()
        table_widget = self.create_table()
        data = self.load_table_data()
        data = data['record']
        table_widget.set_data(data)
        page_context.add_widget(table_widget)
        return HttpResponse(page_context.render())

class SendMessageContactUs(common_actions.BaseAction):
    def POST(self):
        components.PageStore(self.get_container()).contact_us(self.params)
        return HttpResponse('1')

class ChangeLanguage(common_actions.BaseAction):
    def GET(self):
        # data = components.PageStore(self.get_container()).get_lang_text(self.params['id'])
        # if 'total_matched' in data:
        #     if data['total_matched'] > 0:
        self.request.session['lang'] = self.params['id']
        return HttpResponseRedirect('/')
