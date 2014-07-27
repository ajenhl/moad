from django.shortcuts import get_object_or_404, render
from haystack.views import FacetedSearchView

import attribution.models
import attribution.utils


def home_display (request):
    return render(request, 'attribution/display/home.html')

def person_display (request, person_id):
    person = get_object_or_404(attribution.models.Person, pk=person_id)
    context = {'person': person}
    return render(request, 'attribution/display/person.html', context)

def person_list_display (request):
    context = {'people': attribution.models.Person.objects.all()}
    return render(request, 'attribution/display/person_list.html', context)

def source_display (request, source_id):
    source = get_object_or_404(attribution.models.Source, pk=source_id)
    context = {'source': source}
    return render(request, 'attribution/display/source.html', context)

def source_list_display (request):
    context = {'sources': attribution.models.Source.objects.all()}
    return render(request, 'attribution/display/source_list.html', context)

def text_display (request, text_id):
    text = get_object_or_404(attribution.models.Text, pk=text_id)
    assertions = text.assertions
    summary = attribution.utils.get_text_summary(assertions)
    context = {'text': text, 'assertions': assertions, 'summary': summary}
    return render(request, 'attribution/display/text.html', context)


class TextSearchView (FacetedSearchView):

    def extra_context (self):
        extra = super(TextSearchView, self).extra_context()
        query_parameters = self.request.GET.copy()
        query_parameters.pop('page', None)
        extra['query_parameters'] = query_parameters
        full_path = self.request.get_full_path()
        if '?' not in full_path:
            full_path += '?'
        extra['full_path'] = full_path
        return extra
