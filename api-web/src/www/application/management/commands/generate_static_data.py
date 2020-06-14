import json, pika, os
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from notasquare.urad_api.containers.standard import Container
from application.models import *
from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        text = ''
        with open("static-data/impression.txt") as f:
            text = f.readline()

        page_im = Page()
        page_im.title = 'Impression'
        page_im.content = text
        page_im.save()
        print "[*] Create page [Impression]. Done \n"

        with open("static-data/term-of-use.txt") as f:
            text = f.readline()

        page_term = Page()
        page_term.title = 'Term of use'
        page_term.content = text
        page_term.save()

        print "[*] Create page [Term of use]. Done \n"

        with open("static-data/privacy.txt") as f:
            text = f.readline()

        page_pri = Page()
        page_pri.title = 'Privacy'
        page_pri.content = text
        page_pri.save()

        print "[*] Create page Privacy. Done \n"

        with open("static-data/copyright.txt") as f:
            text = f.readline()

        page_cp = Page()
        page_cp.title = 'Copyright'
        page_cp.content = text
        page_cp.save()

        print "[*] Create page [Copyright]. Done \n"

        contact_text = "<p>Genopedia Headquaters<br>Saalachstrasse 92<br>5020 Salzburg<br>Austria<br>info@genopedia.com</p>"
        about_text = "<p>Genopedia is an open and free database on human genetics. It's goal is to capture all that is known about humen genes, genetic diseases, mutations, genetic variations and their effects. By using crowd sourcing and Deep Genome AI (our artificial inteligence engine), all new and existing science on human genetics is scanned and captured to the best of our abilities to create this open resource for everyone. Everyone of us is unique and Genopedia attempts to tell us how.</p>"

        query = ApplicationSetting.objects.filter()
        page_setting = ApplicationSetting()
        if query:
            page_setting = query[0]
        page_setting.application_title = 'Front setting'
        page_setting.contact_address_text = contact_text
        page_setting.about_genopedia_text = about_text
        page_setting.copyright_page_id = page_cp.id
        page_setting.impression_page_id = page_im.id
        page_setting.privacy_page_id = page_pri.id
        page_setting.term_of_use_page_id = page_term.id
        page_setting.save()

        print '[*]'+ '='*10+ " Insert static data done!"
