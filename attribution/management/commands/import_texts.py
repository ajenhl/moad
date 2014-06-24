import csv

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

import attribution.models


class Command (BaseCommand):

    args = '<CSV file> <source_id>'
    help = 'Imports text identifiers and titles from a CSV file'

    @transaction.atomic
    def handle (self, *args, **options):
        if len(args) != 2:
            raise CommandError(
                'A single CSV file and source ID must be supplied')
        filename, source_id = args
        try:
            source = attribution.models.Source.objects.get(pk=int(source_id))
        except attribution.models.Source.DoesNotExist:
            raise CommandError('Source "%s" does not exist' % source_id)
        with open(filename, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self._add_text(source, *row)

    def _add_text (self, source, identifier, title):
        assertion = attribution.models.PropertyAssertion.objects.create(
            is_preferred=False, source=source)
        text = attribution.models.Text.objects.create()
        assertion.texts.add(text)
        identifier = attribution.models.Identifier.objects.create(
            name=identifier, assertion=assertion)
        title = attribution.models.Title.objects.create(
            assertion=assertion, name=title)
