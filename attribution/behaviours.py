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

    def __unicode__ (self):
        return self.name


class Notable (models.Model):

    notes = models.TextField(blank=True)

    class Meta:
        abstract = True


class Publishable (models.Model):

    status = models.CharField(choices=PUBLICATION_STATUSES,
                              default=DRAFT_STATUS, max_length=2)

    class Meta:
        abstract = True


class SortDatable (models.Model):

    sort_date = models.IntegerField(
        blank=True, null=True, help_text='Year used for sorting purposes')

    class Meta:
        abstract = True
