from django.db import models

from .behaviours import Namable
import constants


class Text (models.Model):

    def _get_property_assertions (self, property_name):
        lookup = '{}__isnull'.format(property_name)
        return self.assertions.filter(**{lookup: False}).order_by(
            'is_preferred')

    def __unicode__ (self):
        id_assertions = self._get_property_assertions(
            constants.IDENTIFIER_PROPERTY)
        ids = id_assertions.values_list('identifier', flat=True)
        return '; '.join(ids) or '[No identifier supplied]'


class Date (models.Model):

    date = models.CharField(max_length=200)


class Identifier (Namable, models.Model):

    assertion = models.ForeignKey('PropertyAssertion')


class Person (Namable, models.Model):

    pass


class Source (models.Model):

    name = models.TextField()

    def __unicode__ (self):
        return self.name


class Title (Namable, models.Model):

    pass


class PropertyAssertion (models.Model):

    texts = models.ManyToManyField(Text, related_name='assertions')
    titles = models.ManyToManyField(Title, null=True)
    authors = models.ManyToManyField(Person, null=True, related_name='authored')
    translators = models.ManyToManyField(Person, null=True,
                                         related_name='translated')
    source = models.ForeignKey(Source)
    source_detail = models.TextField(blank=True)
    argument = models.TextField(blank=True)
    is_preferred = models.BooleanField()
