from django.db import models
from django.shortcuts import get_object_or_404, render

from ddh_utils.views import FacetedSearchView

from attribution.forms import RESULTS_PER_PAGE
from attribution.models import Date, Person, PropertyAssertion, Source, Text
import attribution.utils


def home_display (request):
    return render(request, 'attribution/display/home.html')

def date_display (request, date):
    people = Person.objects.filter(sort_date=date)
    assertions = PropertyAssertion.objects.filter(
        models.Q(dates__sort_date=date) |
        models.Q(people__sort_date=date))
    context = {'date': date, 'people': people, 'assertions': assertions}
    return render(request, 'attribution/display/date.html', context)

def date_list_display (request):
    dates = list(set(list(Date.objects.values_list('sort_date', flat=True)) + \
                     list(Person.objects.values_list('sort_date', flat=True))))
    dates = [date for date in dates if date]
    dates.sort()
    context = {'dates': dates}
    return render(request, 'attribution/display/date_list.html', context)

def person_display (request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    context = {'person': person, 'assertions': person.get_assertions()}
    return render(request, 'attribution/display/person.html', context)

def source_display (request, source_id):
    source = get_object_or_404(Source, pk=source_id)
    context = {'source': source}
    return render(request, 'attribution/display/source.html', context)

def text_display (request, text_id):
    text = get_object_or_404(Text, pk=text_id)
    assertions = text.assertions
    summary = attribution.utils.get_text_summary(assertions)
    context = {'text': text, 'assertions': assertions, 'summary': summary}
    return render(request, 'attribution/display/text.html', context)


class ModelSearchView (FacetedSearchView):

    def build_page (self):
        # Allow for the number of results per page to be set
        # dynamically.
        if self.form.is_valid():
            self.results_per_page = self.form.cleaned_data['results_per_page']
        else:
            self.results_per_page = RESULTS_PER_PAGE
        return super(ModelSearchView, self).build_page()
