import re
import unicodedata

from django import template


register = template.Library()


@register.filter
def remove_combining (text):
    if type(text) != type(''):
        text = text.decode('utf-8')
    nkfd_form = unicodedata.normalize('NFKD', text)
    return u''.join([c for c in nkfd_form if not unicodedata.combining(c)])

@register.filter
def split_identifier (text):
    if type(text) != type(''):
        text = text.decode('utf-8')
    match = re.search(r'^(JB|T|X|ZW)([0-9]+)$', text)
    if match is not None:
        number_zeros = 4 - len(match.group(2))
        zero_filled = match.group(1) + (number_zeros * '0') + match.group(2)
        text = '{} {} {} {}'.format(text, match.group(1), match.group(2),
                                    zero_filled)
    return text
