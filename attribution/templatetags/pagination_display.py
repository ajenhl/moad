from django import template


register = template.Library()

@register.inclusion_tag('attribution/display/pagination.html')
def show_pagination (num_pages, current_page, query_parameters):
    """Renders a pagination template with appropriate links."""
    data = {}
    query_string = query_parameters.urlencode()
    if query_string:
        query_string = '&%s' % query_string
    data['query_string'] = query_string
    first_page = max(current_page - 3, 1)
    last_page = min(current_page + 3, num_pages)
    data['pre_pages'] = range(first_page, current_page)
    data['post_pages'] = range(current_page + 1, last_page + 1)
    data['current_page'] = current_page
    data['first_link'] = first_page < current_page
    data['last_link'] = last_page > current_page
    data['last_page'] = num_pages
    return data
