def _assemble_preferred_assertion_data (assertion, property_name):
    data = None
    if assertion is not None:
        value = '; '.join([unicode(prop) for prop in getattr(assertion, property_name).all()])
        data = {'value': value, 'id': assertion.pk,
                'source': assertion.source.abbreviation}
    return data

def _get_preferred_assertion (assertions, property_name):
    lookup = '%s__isnull' % property_name
    query = {lookup: False}
    all_properties = assertions.filter(**query)
    preferred_properties = all_properties.filter(is_preferred=True)
    if preferred_properties:
        return preferred_properties[0]
    elif all_properties:
        return all_properties[0]
    else:
        return None

def _get_summary_data (assertions, property_name):
    assertion = _get_preferred_assertion(assertions, property_name)
    return _assemble_preferred_assertion_data(assertion, property_name)

def get_text_summary (assertions):
    data = {
        'author': _get_summary_data(assertions, 'authors'),
        'date': _get_summary_data(assertions, 'dates'),
        'identifier': _get_summary_data(assertions, 'identifiers'),
        'title': _get_summary_data(assertions, 'titles'),
        'translator': _get_summary_data(assertions, 'translators'),
    }
    return data
