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

    class Meta:
        ordering = ['cached_identifier__identifier']

    def get_absolute_url (self):
        return reverse('text_display', args=[str(self.id)])

    def generate_identifier (self):
        """Generates a composite identifier from the texts identifiers and
        titles."""
        identifiers = self.get_identifiers()
        titles = self.get_titles()
        identifier = u'; '.join(identifiers + titles)
        return identifier or u'[No identifier supplied]'

    def get_authors (self):
        return Person.objects.filter(authored__texts=self)

    def get_authorship_dates (self):
        """Returns a list of all author sort dates associated with this
        Text."""
        authors = self.get_authors()
        return list(authors.values_list('sort_date', flat=True))

    def get_dates (self):
        """Returns a list of all sort dates associated with this Text."""
        return list(set(self.get_authorship_dates() +
                        self.get_translation_dates() +
                        self.get_text_dates()))

    def get_identifiers (self):
        """Returns a list of all identifiers associated with this Text."""
        identifiers = Identifier.objects.filter(assertion__texts=self)
        return list(identifiers.values_list('name', flat=True))

    def get_people (self):
        """Returns a list of all people associated with this Text."""
        return list(self.get_authors().values_list('id', flat=True)) + \
            list(self.get_translators().values_list('id', flat=True))

    def get_preferred_dates (self):
        """Returns the preferred dates associated with this Text.

        These dates are drawn from the assertion directly, and from
        translators and authors. Where the same assertion specifies
        both a date and a dated person, the date is used and not the
        person's date.

        """
        dates = []
        assertions = self.assertions
        preferred_assertions = assertions.filter(is_preferred=True)
        # First get dates from assertions marked as preferred.
        for assertion in preferred_assertions:
            dates.extend(assertion.get_preferred_dates())
        # Use the most recent non-preferred assertion that has a date
        # if no date has yet been found.
        if not dates:
            try:
                assertion = assertions.filter(
                    models.Q(dates__sort_date__isnull=False) |
                    models.Q(authors__sort_date__isnull=False) |
                    models.Q(translators__sort_date__isnull=False))[0]
                dates.extend(assertion.get_preferred_dates())
            except IndexError:
                pass
        return list(set(dates))

    def get_sources (self):
        """Returns all sources associated with this Text."""
        sources = Source.objects.filter(assertions__texts=self)
        return list(sources.values_list('id', flat=True))

    def get_text_dates (self):
        """Returns a list of all non-author, non-translator sort dates
        associated with this Text."""
        dates = Date.objects.filter(assertion__texts=self)
        return list(dates.values_list('sort_date', flat=True))

    def get_titles (self):
        """Returns a list of all titles associated with this Text."""
        titles = Title.objects.filter(assertion__texts=self)
        return list(titles.values_list('name', flat=True))

    def get_translators (self):
        return Person.objects.filter(translated__texts=self)

    def get_translation_dates (self):
        """"Returns a list of all translator sort dates associated with this
        Text."""
        translators = self.get_translators()
        return list(translators.values_list('sort_date', flat=True))

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

    def get_preferred_dates (self):
        """Returns a list of distinct sort dates associated with this
        PropertyAssertion.

        Not all dates are necessarily returned. If the assertion has a
        directly specified date, that is used; otherwise dates
        associated with authors and translators are used.

        """
        # Use dates directly associated with the assertion.
        new_dates = self.dates.all()
        dates = [date.sort_date for date in new_dates if date]
        if not dates:
            # In the absence of direct dates, use dates associated
            # with the translators and authors.
            author_dates = self.authors.values_list('sort_date', flat=True)
            translator_dates = self.translators.values_list(
                'sort_date', flat=True)
            sort_dates = list(author_dates) + list(translator_dates)
            dates = [sort_date for sort_date in sort_dates if sort_date]
        return dates

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
