import os.path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.loader import get_template

from lxml import etree

from ...constants import SOURCE_ABBREVIATIONS_WITH_PREDICATES
from ...models import Person, PropertyAssertion, Source, Text


class Command (BaseCommand):

    help = 'Generates and saves full RDF export'

    def handle(self, *args, **options):
        assertions = PropertyAssertion.published_objects.all()
        people = Person.published_objects.all()
        sources = Source.published_objects.all()
        texts = Text.published_objects.all()
        template = get_template('attribution/display/all_rdf.xml')
        context = {
            'assertions': assertions,
            'people': people,
            'sources': sources,
            'source_abbreviations': SOURCE_ABBREVIATIONS_WITH_PREDICATES,
            'texts': texts
        }
        output = os.path.join(settings.BASE_DIR,
                              'attribution/static/all_rdf.xml')
        parser = etree.XMLParser(remove_blank_text=True)
        root = etree.fromstring(template.render(context).encode('utf-8'),
                                parser)
        tree = etree.ElementTree(root)
        tree.write(output, encoding='utf-8', pretty_print=True,
                   xml_declaration=True)
