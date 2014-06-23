from django.shortcuts import get_object_or_404, render

import attribution.models


def person_display (request, person_id):
    person = get_object_or_404(attribution.models.Person, pk=person_id)
    context = {'person': person}
    return render(request, 'attribution/display/person.html', context)

def person_list_display (request):
    people = attribution.models.Person.objects.all()
    context = {'people': people}
    return render(request, 'attribution/display/person_list.html', context)

def text_display (request, text_id):
    text = get_object_or_404(attribution.models.Text, pk=text_id)
    assertions = text.assertions.order_by('is_preferred')
    context = {'text': text, 'assertions': assertions}
    return render(request, 'attribution/display/text.html', context)

def text_list_display (request):
    texts = attribution.models.Text.objects.all()
    context = {'texts': texts}
    return render(request, 'attribution/display/text_list.html', context)
