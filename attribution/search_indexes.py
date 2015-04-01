from haystack import indexes

from .models import Person, PersonRole, PropertyAssertion, Source, Text
from .search_fields import IntegerMultiValueField, FacetIntegerMultiValueField


class PersonIndex (indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    full_date = indexes.CharField(indexed=False, model_attr='date')
    date = indexes.IntegerField(faceted=True, model_attr='sort_date',
                                null=True)
    name = indexes.CharField(indexed=False, model_attr='name', null=True)
    role = indexes.MultiValueField(faceted=True, null=True)
    source = indexes.MultiValueField(faceted=True, null=True)
    texts = indexes.MultiValueField(faceted=True, null=True)

    def get_model (self):
        return Person

    def prepare_role (self, person):
        return list(PersonRole.objects.filter(involvements__person=person).distinct().values_list('name', flat=True))

    def prepare_source (self, person):
        return list(Source.objects.filter(assertions__people=person).distinct().values_list('id', flat=True))

    def prepare_texts (self, person):
        return list(Text.objects.filter(assertions__people=person).distinct().values_list('id', flat=True))


class PropertyAssertionIndex (indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)

    def get_model (self):
        return PropertyAssertion


class SourceIndex (indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    date = indexes.IntegerField(faceted=True, null=True)

    def get_model (self):
        return Source


class TextIndex (indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    identifier = indexes.CharField(indexed=False,
                                   model_attr='cached_identifier')
    date = IntegerMultiValueField(
        faceted=True, facet_class=FacetIntegerMultiValueField,
        model_attr='get_dates', null=True)
    preferred_date = IntegerMultiValueField(
        faceted=True, model_attr='get_preferred_dates', null=True,
        facet_class=FacetIntegerMultiValueField)
    person = indexes.MultiValueField(faceted=True, null=True)
    source = indexes.MultiValueField(faceted=True, model_attr='get_sources',
                                     null=True)

    def get_model (self):
        return Text

    def index_queryset (self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def prepare_person (self, text):
        people = text.get_people()
        return [person.id for person in people]
