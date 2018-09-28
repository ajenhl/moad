from django.core.management.base import BaseCommand
from django.template.loader import get_template

from ...models import Person, PropertyAssertion, Source, Text


class Command (BaseCommand):

    help = 'Generates and saves full RDF export'

    def handle(self, *args, **options):
        assertions = PropertyAssertion.published_objects.all()
        people = Person.published_objects.all()
        sources = Source.published_objects.all()
        texts = Text.published_objects.all()
        template = get_template('attribution/display/all_rdf.xml')
        context = {'assertions': assertions,
                   'people': people,
                   'sources': sources,
                   'texts': texts}
        with open('attribution/static/all_rdf.xml', 'w') as fh:
            fh.write(template.render(context))
