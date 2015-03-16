import unicodedata

from django import template


register = template.Library()


@register.filter
def remove_combining (text):
    nkfd_form = unicodedata.normalize('NFKD', text)
    return u''.join([c for c in nkfd_form if not unicodedata.combining(c)])
