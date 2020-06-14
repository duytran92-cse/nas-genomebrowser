from django.template import Library

import json

register = Library()

@register.filter(name='math')
def math(o, total):
    try:
        return (float(o)/float(total))*100
    except:
        pass

@register.filter(name='shorter')
def shorter(o, total):
    try:
        return round((float(o)/float(total)) * 100, 2 )
    except:
        pass
