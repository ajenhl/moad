from django.db import models

from .behaviours import PUBLISHED_STATUS


class PublishedManager (models.Manager):

    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(
            status=PUBLISHED_STATUS)
