from django import template

from ..models import Person, Source, Text


register = template.Library()

def _render_facet (query_parameters, facet_field, facet_name,
                   facet_display_name, facet_count, view=None):
    parameters = query_parameters.copy()
    data = {'add_facet_url': None,
            'facet_count': facet_count,
            'facet_display_name': facet_display_name,
            'facet_name': facet_name,
            'remove_facet_url': None,
            'view': view}
    facet_key = u'selected_facets'
    facet_value = u'%s:%s' % (facet_field, facet_name)
    facets = parameters.getlist(facet_key)
    try:
        facets.remove(facet_value)
        url_key = 'remove_facet_url'
    except ValueError:
        facets.append(facet_value)
        url_key = 'add_facet_url'
    parameters.setlist(facet_key, facets)
    data[url_key] = '?%s' % parameters.urlencode()
    return data

@register.inclusion_tag('attribution/display/facet.html')
def render_date_facet (query_parameters, facet_field, facet):
    """Renders a facet display template with links to add, remove, and
    view the specified date facet."""
    facet_name, facet_count = facet
    return _render_facet(query_parameters, facet_field, facet_name,
                         facet_name, facet_count, 'date_display')


@register.inclusion_tag('attribution/display/facet.html')
def render_person_facet (query_parameters, facet_field, facet):
    """Renders a facet display template with links to add, remove, and
    view the specified person facet."""
    facet_name, facet_count = facet
    person = Person.objects.get(pk=int(facet_name))
    return _render_facet(query_parameters, facet_field, facet_name,
                         str(person), facet_count, 'person_display')

@register.inclusion_tag('attribution/display/facet.html')
def render_source_facet (query_parameters, facet_field, facet):
    """Renders a facet display template with links to add, remove, and
    view the specified source facet."""
    facet_name, facet_count = facet
    source = Source.objects.get(pk=int(facet_name))
    return _render_facet(query_parameters, facet_field, facet_name,
                         source.abbreviation, facet_count, 'source_display')

@register.inclusion_tag('attribution/display/facet.html')
def render_text_facet (query_parameters, facet_field, facet):
    """Renders a facet display template with links to add, remove, and
    view the specified text facet."""
    facet_name, facet_count = facet
    text = Text.objects.get(pk=int(facet_name))
    return _render_facet(query_parameters, facet_field, facet_name,
                         str(text), facet_count, 'text_display')

@register.inclusion_tag('attribution/display/facet.html')
def render_unlinked_facet (query_parameters, facet_field, facet):
    """Renders a facet display template with links to add and remove the
    specified facet. This facet has no independent display on the
    site."""
    facet_name, facet_count = facet
    return _render_facet(query_parameters, facet_field, facet_name,
                         facet_name, facet_count)
