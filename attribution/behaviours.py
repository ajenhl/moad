from urllib.parse import urljoin

from django.contrib.sites.models import Site
from django.db import models


DRAFT_STATUS = 'DR'
PUBLISHED_STATUS = 'PU'
PUBLICATION_STATUSES = [
    (DRAFT_STATUS, 'Draft'),
    (PUBLISHED_STATUS, 'Published'),
    ]


class Namable (models.Model):

    name = models.CharField(max_length=500,
                            help_text='Separate multiple names with ", "')

    class Meta:
        abstract = True

    def __str__(self):
        return self.name.strip()

    def get_names(self):
        return self.name.split(', ')


class Notable (models.Model):

    notes = models.TextField(blank=True)

    class Meta:
        abstract = True


class Publishable (models.Model):

    status = models.CharField(choices=PUBLICATION_STATUSES,
                              default=DRAFT_STATUS, max_length=2)

    class Meta:
        abstract = True


class Referenceable:

    def get_reference_uri(self):
        site = Site.objects.get_current()
        return urljoin('https://{}'.format(site.domain),
                       self.get_absolute_url())


class SortDatable (models.Model):

    sort_date = models.IntegerField(
        blank=True, null=True, help_text='Year used for sorting purposes')

    class Meta:
        abstract = True
