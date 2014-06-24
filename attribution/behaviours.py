from django.db import models


class Namable (models.Model):

    name = models.CharField(max_length=500,
                            help_text='Separate multiple names with " / "')

    class Meta:
        abstract = True

    def __unicode__ (self):
        return self.name


class Notable (models.Model):

    notes = models.TextField(blank=True)

    class Meta:
        abstract = True
