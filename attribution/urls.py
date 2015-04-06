from django.conf.urls import patterns, url
from haystack.query import SearchQuerySet
from haystack.views import search_view_factory

from .forms import ModelSearchForm
from .models import Person, Source, Text
from .views import ModelSearchView


urlpatterns = patterns('attribution.views',
    url(r'^$', 'home_display', name='home_display'),
    url(r'^date/$', 'date_list_display', name='date_list_display'),
    url(r'^date/(?P<date>-?\d+)/$', 'date_display', name='date_display'),
    url(r'^person/(?P<person_id>\d+)/$', 'person_display',
        name='person_display'),
    url(r'^source/(?P<source_id>\d+)/$', 'source_display',
        name='source_display'),
    url(r'^text/(?P<text_id>\d+)/$', 'text_display', name='text_display'),
)

# Search.

person_sqs = SearchQuerySet().models(Person).facet('sort_date').facet('source').facet('role').facet('texts').order_by('name')

source_sqs = SearchQuerySet().models(Source).facet('date').order_by('date')

text_sqs = SearchQuerySet().models(Text).facet('date').facet('person').facet('source').facet('preferred_date').order_by('identifier')

urlpatterns += patterns('attribution.views',
    url(r'^person/$', search_view_factory(
        form_class=ModelSearchForm, view_class=ModelSearchView,
        searchqueryset=person_sqs,
        template='attribution/display/person_list.html'),
        name='person_list_display'),
    url(r'^source/$', search_view_factory(
        form_class=ModelSearchForm, view_class=ModelSearchView,
        searchqueryset=source_sqs,
        template='attribution/display/source_list.html'),
        name='source_list_display'),
    url(r'^text/$', search_view_factory(
        form_class=ModelSearchForm, view_class=ModelSearchView,
        searchqueryset=text_sqs,
        template='attribution/display/text_list.html'),
        name='text_list_display'),
)
