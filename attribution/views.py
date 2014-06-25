from django.shortcuts import get_object_or_404, render

import attribution.models
import attribution.utils


def home_display (request):
    return render(request, 'attribution/display/home.html')

def person_display (request, person_id):
    person = get_object_or_404(attribution.models.Person, pk=person_id)
    context = {'person': person}
    return render(request, 'attribution/display/person.html', context)

def person_list_display (request):
    people = attribution.models.Person.objects.all()
    context = {'people': people}
    return render(request, 'attribution/display/person_list.html', context)

def source_display (request, source_id):
    source = get_object_or_404(attribution.models.Source, pk=source_id)
    context = {'source': source}
    return render(request, 'attribution/display/source.html', context)

def source_list_display (request):
    sources = attribution.models.Source.objects.all()
    context = {'sources': sources}
    return render(request, 'attribution/display/source_list.html', context)

def text_display (request, text_id):
    text = get_object_or_404(attribution.models.Text, pk=text_id)
    assertions = text.assertions
    summary = attribution.utils.get_text_summary(assertions)
    context = {'text': text, 'assertions': assertions, 'summary': summary}
    return render(request, 'attribution/display/text.html', context)

def text_list_display (request):
    texts = attribution.models.Text.objects.select_related('cached_identifier').order_by(
        'cached_identifier__identifier')
    context = {'texts': texts}
    return render(request, 'attribution/display/text_list.html', context)
