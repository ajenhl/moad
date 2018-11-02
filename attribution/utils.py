from attribution.models import PersonRole


def _assemble_preferred_assertion_data(assertion, property_name):
    data = None
    if assertion is not None:
        value = '; '.join([str(prop) for prop
                           in getattr(assertion, property_name).all()])
        data = {'value': value, 'id': assertion.pk,
                'sources': [source.abbreviation for source
                            in assertion.sources.all()]}
    return data


def _get_person_summary_data(assertions):
    data = {}
    for role in PersonRole.objects.all():
        all_assertions = assertions.filter(person_involvements__role=role)
        preferred_assertions = all_assertions.filter(is_preferred=True)
        if preferred_assertions:
            assertion = preferred_assertions[0]
        elif all_assertions:
            assertion = all_assertions[0]
        else:
            continue
        value = '; '.join([str(person) for person in
                           assertion.people.filter(involvements__role=role)])
        data[role] = {'value': value, 'id': assertion.pk,
                      'sources': [source.abbreviation for source
                                  in assertion.sources.all()]}
    return data


def _get_preferred_assertion(assertions, property_name):
    lookup = '{}__isnull'.format(property_name)
    query = {lookup: False}
    all_properties = assertions.filter(**query)
    preferred_properties = all_properties.filter(is_preferred=True)
    if preferred_properties:
        return preferred_properties[0]
    elif all_properties:
        return all_properties[0]
    else:
        return None


def _get_summary_data(assertions, property_name):
    assertion = _get_preferred_assertion(assertions, property_name)
    return _assemble_preferred_assertion_data(assertion, property_name)


def get_text_summary(assertions):
    data = {
        'date': _get_summary_data(assertions, 'dates'),
        'identifier': _get_summary_data(assertions, 'identifiers'),
        'people': _get_person_summary_data(assertions),
        'title': _get_summary_data(assertions, 'titles'),
    }
    return data
