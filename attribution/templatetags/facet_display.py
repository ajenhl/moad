from django import template

from ..models import Person, Source


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
def render_facet (query_parameters, facet_field, facet):
    """Renders a facet display template with links to add and remove the
    specified facet.."""
    facet_name, facet_count = facet
    return _render_facet(query_parameters, facet_field, facet_name,
                         facet_name, facet_count)


@register.inclusion_tag('attribution/display/facet.html')
def render_person_facet (query_parameters, facet_field, facet):
    facet_name, facet_count = facet
    person = Person.objects.get(pk=int(facet_name))
    return _render_facet(query_parameters, facet_field, facet_name,
                         unicode(person), facet_count, 'person_display')

@register.inclusion_tag('attribution/display/facet.html')
def render_source_facet (query_parameters, facet_field, facet):
    facet_name, facet_count = facet
    source = Source.objects.get(pk=int(facet_name))
    return _render_facet(query_parameters, facet_field, facet_name,
                         source.abbreviation, facet_count, 'source_display')
