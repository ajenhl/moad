from haystack import indexes


class IntegerMultiValueField (indexes.MultiValueField):

    field_type = 'integer'


class FacetIntegerMultiValueField (indexes.FacetField, IntegerMultiValueField):

    pass
