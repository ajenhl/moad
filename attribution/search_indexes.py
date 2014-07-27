from haystack import indexes

from .models import Text
from .search_fields import IntegerMultiValueField, FacetIntegerMultiValueField


class TextIndex (indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    date = IntegerMultiValueField(
        faceted=True, facet_class=FacetIntegerMultiValueField,
        model_attr='get_dates', null=True)
    preferred_date = IntegerMultiValueField(
        faceted=True, model_attr='get_preferred_dates', null=True,
        facet_class=FacetIntegerMultiValueField)
    person = indexes.MultiValueField(faceted=True, model_attr='get_people',
                                     null=True)
    source = indexes.MultiValueField(faceted=True, model_attr='get_sources',
                                     null=True)

    def get_model (self):
        return Text

    def index_queryset (self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
