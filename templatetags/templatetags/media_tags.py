from django import template
import re

register = template.Library()

@register.filter
def media(field):
    try:
        return re.sub('^.*/media/', '/media/', field)
    except:
        return ""
