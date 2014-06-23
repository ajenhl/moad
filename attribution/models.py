from django.db import models

from .behaviours import Namable, Notable


class Date (Namable, Notable, models.Model):

    assertion = models.ForeignKey('PropertyAssertion',
                                  related_name='dates')


class Identifier (Namable, Notable, models.Model):

    assertion = models.ForeignKey('PropertyAssertion',
                                  related_name='identifiers')


class Person (Namable, Notable, models.Model):

    class Meta:
        ordering = ['name']


class Source (models.Model):

    name = models.TextField(help_text='Full bibliographic details')
    date = models.CharField(max_length=5, help_text='Format: YYYY')
    abbreviation = models.CharField(
        max_length=10, help_text='Bibliographic reference, eg. Nat1992')

    class Meta:
        ordering = ['-date']

    def autocomplete_search_fields ():
        return ('id__iexact', 'name__icontains')

    def __unicode__ (self):
        return self.name


class Text (models.Model):

    def __unicode__ (self):
        ids = Identifier.objects.filter(assertion__texts=self).values_list(
            'name', flat=True)
        return u'; '.join(ids) or u'[No identifier supplied]'


class Title (Namable, models.Model):

    assertion = models.ForeignKey('PropertyAssertion',
                                  related_name='titles')

    @staticmethod
    def autocomplete_search_fields ():
        return ('id__iexact', 'name__icontains')


class PropertyAssertion (models.Model):

    texts = models.ManyToManyField(Text, related_name='assertions')
    authors = models.ManyToManyField(Person, blank=True, null=True,
                                     related_name='authored')
    translators = models.ManyToManyField(Person, blank=True, null=True,
                                         related_name='translated')
    source = models.ForeignKey(Source)
    source_detail = models.TextField(blank=True)
    argument = models.TextField(blank=True)
    is_preferred = models.BooleanField()

    class Meta:
        ordering = ['source']

    def __unicode__ (self):
        argument = u'[No argument provided]'
        if self.argument:
            argument = u'%s...' % self.argument[:30]
        return argument
