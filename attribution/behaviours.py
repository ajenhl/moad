from django.db import models


class Namable (models.Model):

    name = models.CharField(max_length=200)

    class Meta:
        abstract = True

    def __unicode__ (self):
        return self.name
