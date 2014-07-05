from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
    person_list = attribution.models.Person.objects.all()
    filter_text = request.GET.get('q', '')
    if filter_text:
        person_list = person_list.filter(name__icontains=filter_text)
    paginator = Paginator(person_list, 50)
    page = request.GET.get('page')
    query_parameters = request.GET.copy()
    query_parameters.pop('page', None)
    try:
        people = paginator.page(page)
    except PageNotAnInteger:
        people = paginator.page(1)
    except EmptyPage:
        people = paginator.page(paginator.num_pages)
    context = {'current_page': people.number, 'filter': filter_text,
               'num_pages': paginator.num_pages, 'people': people,
               'query_parameters': query_parameters}
    return render(request, 'attribution/display/person_list.html', context)

def source_display (request, source_id):
    source = get_object_or_404(attribution.models.Source, pk=source_id)
    context = {'source': source}
    return render(request, 'attribution/display/source.html', context)

def source_list_display (request):
    source_list = attribution.models.Source.objects.all()
    filter_text = request.GET.get('q', '')
    if filter_text:
        source_list = source_list.filter(name__icontains=filter_text)
    paginator = Paginator(source_list, 50)
    page = request.GET.get('page')
    query_parameters = request.GET.copy()
    query_parameters.pop('page', None)
    try:
        sources = paginator.page(page)
    except PageNotAnInteger:
        sources = paginator.page(1)
    except EmptyPage:
        sources = paginator.page(paginator.num_pages)
    context = {'current_page': sources.number, 'filter': filter_text,
               'num_pages': paginator.num_pages, 'sources': sources,
               'query_parameters': query_parameters}
    return render(request, 'attribution/display/source_list.html', context)

def text_display (request, text_id):
    text = get_object_or_404(attribution.models.Text, pk=text_id)
    assertions = text.assertions
    summary = attribution.utils.get_text_summary(assertions)
    context = {'text': text, 'assertions': assertions, 'summary': summary}
    return render(request, 'attribution/display/text.html', context)

def text_list_display (request):
    text_list = attribution.models.Text.objects.select_related('cached_identifier').order_by('cached_identifier__identifier')
    filter_text = request.GET.get('q', '')
    if filter_text:
        text_list = text_list.filter(
            cached_identifier__identifier__icontains=filter_text)
    paginator = Paginator(text_list, 50)
    page = request.GET.get('page')
    query_parameters = request.GET.copy()
    query_parameters.pop('page', None)
    try:
        texts = paginator.page(page)
    except PageNotAnInteger:
        texts = paginator.page(1)
    except EmptyPage:
        texts = paginator.page(paginator.num_pages)
    context = {'current_page': texts.number, 'filter': filter_text,
               'num_pages': paginator.num_pages, 'texts': texts,
               'query_parameters': query_parameters}
    return render(request, 'attribution/display/text_list.html', context)
