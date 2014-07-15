from django.core.urlresolvers import reverse
from django.db import models

from .behaviours import Namable, Notable, SortDatable


class Date (Namable, Notable, SortDatable, models.Model):

    assertion = models.ForeignKey('PropertyAssertion',
                                  related_name='dates')


class Identifier (Namable, Notable, models.Model):

    assertion = models.ForeignKey('PropertyAssertion',
                                  related_name='identifiers')


class Person (Namable, Notable, SortDatable, models.Model):

    date = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def get_absolute_url (self):
        return reverse('person_display', args=[str(self.id)])


class Source (Notable, models.Model):

    name = models.TextField(help_text='Full bibliographic details')
    date = models.CharField(max_length=5, help_text='Format: YYYY. Use the earliest date if there is a range')
    abbreviation = models.CharField(
        max_length=30, help_text='Bibliographic reference, eg. "Nattier 1992"',
        unique=True)

    class Meta:
        ordering = ['-date']

    @staticmethod
    def autocomplete_search_fields ():
        return ('id__iexact', 'name__icontains')

    def get_absolute_url (self):
        return reverse('source_display', args=[str(self.id)])

    def __unicode__ (self):
        return self.name


class TextIdentifierCache (models.Model):

    text = models.OneToOneField('Text', related_name='cached_identifier')
    identifier = models.TextField(blank=True)

    def __unicode__ (self):
        return self.identifier


class Text (models.Model):

    def get_absolute_url (self):
        return reverse('text_display', args=[str(self.id)])

    def generate_identifier (self):
        """Generates a composite identifier from the texts identifiers and
        titles."""
        identifiers = Identifier.objects.filter(assertion__texts=self)
        titles = Title.objects.filter(assertion__texts=self)
        identifier = u'; '.join(
            list(identifiers.values_list('name', flat=True)) + \
            list(titles.values_list('name', flat=True)))
        return identifier or u'[No identifier supplied]'

    def save (self, *args, **kwargs):
        super(Text, self).save(*args, **kwargs)
        identifier = self.generate_identifier()
        try:
            cache = self.cached_identifier
            cache.identifier = identifier
        except TextIdentifierCache.DoesNotExist:
            cache = TextIdentifierCache(text=self, identifier=identifier)
        cache.save()

    def __unicode__ (self):
        return unicode(self.cached_identifier)


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
    source = models.ForeignKey(Source, related_name='assertions')
    source_detail = models.TextField(blank=True)
    argument = models.TextField(blank=True)
    is_preferred = models.BooleanField()

    class Meta:
        verbose_name = 'assertion'
        ordering = ['source']

    def delete (self, *args, **kwargs):
        texts = list(self.texts.all())
        super(PropertyAssertion, self).delete(*args, **kwargs)
        for text in texts:
            text.save()

    def has_other_assertions (self):
        """Returns True if any of the texts associated with this assertion
        have other property assertions."""
        other = PropertyAssertion.objects.exclude(id=self.id).filter(
            texts__assertions__id=self.id).count()
        if other:
            return True
        return False

    def __unicode__ (self):
        argument = u'[No argument provided]'
        if self.argument:
            argument = u'%s...' % self.argument[:30]
        return argument
