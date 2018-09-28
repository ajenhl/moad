from urllib.parse import urljoin

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models

from .behaviours import Namable, Notable, Publishable, Referenceable, \
    SortDatable
from . import constants
from .managers import PublishedManager


class Date (Namable, Notable, SortDatable, models.Model):

    assertion = models.ForeignKey('PropertyAssertion',
                                  related_name='dates')


class Identifier (Namable, Notable, models.Model):

    assertion = models.ForeignKey('PropertyAssertion',
                                  related_name='identifiers')


class Person (Namable, Notable, Publishable, Referenceable, SortDatable,
              models.Model):

    date = models.TextField(blank=True)
    author = models.ForeignKey(User, related_name='authored_persons')

    objects = models.Manager()
    published_objects = PublishedManager()

    class Meta:
        ordering = ['name']

    @staticmethod
    def autocomplete_search_fields():
        return ('id__iexact', 'name__icontains',)

    def get_absolute_url(self):
        return reverse('person_display', args=[str(self.id)])

    def get_assertions(self):
        """Returns a dictionary with PersonRole keys and lists of
        PropertyAssertions values."""
        typed_assertions = {}
        for involvement in self.involvements.all():
            assertions = typed_assertions.setdefault(involvement.role, [])
            assertions.append(involvement.assertion)
        return typed_assertions


class PersonInvolvement (models.Model):

    person = models.ForeignKey('Person', related_name='involvements')
    assertion = models.ForeignKey('PropertyAssertion',
                                  related_name='person_involvements')
    role = models.ForeignKey('PersonRole', related_name='involvements')


class PersonRole (Namable, Notable, Publishable, models.Model):

    predicate_uri = models.CharField(blank=True, max_length=150)

    def get_predicate_element(self):
        # This is horrible.
        uri = self.predicate_uri
        for prefix, base_uri in constants.ONTOLOGY_BASE_URIS.items():
            if uri.startswith(base_uri):
                return '{}:{}'.format(prefix, uri[len(base_uri):])


class Source (Notable, Publishable, Referenceable, models.Model):

    name = models.TextField(help_text='Full bibliographic details')
    date = models.CharField(
        max_length=5,
        help_text='Format: YYYY. Use the earliest date if there is a range')
    abbreviation = models.CharField(
        max_length=30, help_text='Bibliographic reference, eg. "Nattier 1992"',
        unique=True)
    author = models.ForeignKey(User, related_name='authored_sources')

    objects = models.Manager()
    published_objects = PublishedManager()

    class Meta:
        ordering = ['-date']

    @staticmethod
    def autocomplete_search_fields():
        return ('id__iexact', 'name__icontains')

    def get_absolute_url(self):
        return reverse('source_display', args=[str(self.id)])

    def __str__(self):
        return self.name


class Text (Publishable, Referenceable, models.Model):

    identifier = models.TextField(blank=True,
                                  help_text=constants.TEXT_IDENTIFIER_HELP)
    author = models.ForeignKey(User, related_name='authored_texts')

    objects = models.Manager()
    published_objects = PublishedManager()

    class Meta:
        ordering = ['identifier']

    def get_absolute_url(self):
        return reverse('text_display', args=[str(self.id)])

    def generate_identifier(self):
        """Generates a composite identifier from the texts identifiers and
        titles."""
        identifiers = self.get_identifiers()
        titles = self.get_titles()
        identifier = '; '.join(identifiers + titles)
        return identifier or '[No identifier supplied]'

    def get_person_dates(self):
        """Returns a list of all person sort dates associated with this
        Text."""
        people = self.get_people()
        return list(people.values_list('sort_date', flat=True))

    def get_dates(self):
        """Returns a list of all sort dates associated with this Text."""
        return list(set(self.get_person_dates() + self.get_text_dates()))

    def get_identifiers(self):
        """Returns a list of all identifiers associated with this Text."""
        identifiers = Identifier.objects.filter(assertion__texts=self)
        return list(identifiers.values_list('name', flat=True).distinct())

    def get_person_involvements(self):
        """Returns a QuerySet of all person involvements association with this
        Text."""
        return PersonInvolvement.objects.filter(assertion__texts=self)

    def get_people(self):
        """Returns a QuerySet of all people associated with this Text."""
        return Person.objects.filter(involvements__assertion__texts=self)

    def get_preferred_dates(self):
        """Returns the preferred dates associated with this Text.

        These dates are drawn from the assertion directly, and from
        the people involved in the assertion. Where the same assertion
        specifies both a date and a dated person, the date is used and
        not the person's date.

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
                    models.Q(person_involvements__person__sort_date__isnull=False))[0]
                dates.extend(assertion.get_preferred_dates())
            except IndexError:
                pass
        return list(set(dates))

    def get_sources(self):
        """Returns all sources associated with this Text."""
        sources = Source.objects.filter(assertions__texts=self)
        return list(sources.values_list('id', flat=True))

    def get_text_dates(self):
        """Returns a list of all non-person sort dates associated with this
        Text."""
        dates = Date.objects.filter(assertion__texts=self)
        return list(dates.values_list('sort_date', flat=True))

    def get_titles(self):
        """Returns a list of all titles associated with this Text."""
        titles = Title.objects.filter(assertion__texts=self)
        return list(titles.values_list('name', flat=True).distinct())

    def save(self, *args, **kwargs):
        self.identifier = self.generate_identifier()
        super(Text, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.identifier)


class Title (Namable, models.Model):

    assertion = models.ForeignKey('PropertyAssertion',
                                  related_name='titles')

    @staticmethod
    def autocomplete_search_fields():
        return ('id__iexact', 'name__icontains')


class PropertyAssertion (Publishable, Referenceable, models.Model):

    texts = models.ManyToManyField(Text, related_name='assertions')
    people = models.ManyToManyField(Person, through=PersonInvolvement)
    source = models.ForeignKey(Source, related_name='assertions')
    source_detail = models.TextField(blank=True)
    argument = models.TextField(blank=True)
    is_preferred = models.BooleanField(default=False)
    author = models.ForeignKey(User, related_name='authored_assertions')
    contributors = models.ManyToManyField(
        User, blank=True, related_name='contributed_assertions')
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    objects = models.Manager()
    published_objects = PublishedManager()

    class Meta:
        verbose_name = 'assertion'
        ordering = ['source']
        permissions = (
            ('change_assertion_author',
             'Can change the author of an assertion'),
            ('change_assertion_contributors',
             'Can change contributors to an assertion'),
            ('change_assertion_status', 'Can change publication status'),
            # While the following permission is tied to this model, it
            # is used as a convenient way to determine whether a user
            # has permission to change *any* of the publishable model
            # items.
            ('change_published_items', 'Can change published items'),
        )

    def delete(self, *args, **kwargs):
        texts = list(self.texts.all())
        super(PropertyAssertion, self).delete(*args, **kwargs)
        for text in texts:
            text.save()

    def get_absolute_url(self):
        return reverse('assertion_display', args=[str(self.id)])

    def get_argument_reference_uri(self):
        site = Site.objects.get_current()
        return urljoin('https://{}'.format(site.domain),
                       reverse('argument_display', args=[str(self.id)]))

    def get_preferred_dates(self):
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
            # with the people involved.
            person_dates = Person.objects.filter(
                involvements__assertion=self).values_list('sort_date',
                                                          flat=True)
            dates = [date for date in list(person_dates) if date]
        return dates

    def has_other_assertions(self):
        """Returns True if any of the texts associated with this assertion
        have other property assertions."""
        other = PropertyAssertion.objects.exclude(id=self.id).filter(
            texts__assertions__id=self.id).count()
        if other:
            return True
        return False

    def __str__(self):
        argument = '[No argument provided]'
        if self.argument:
            argument = '{}...'.format(self.argument[:30])
        return argument
