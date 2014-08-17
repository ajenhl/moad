from django.conf.urls import patterns, url
from haystack.query import SearchQuerySet
from haystack.views import search_view_factory

from .forms import TextSearchForm
from .views import TextSearchView


urlpatterns = patterns('attribution.views',
    url(r'^$', 'home_display', name='home_display'),
    url(r'^date/$', 'date_list_display', name='date_list_display'),
    url(r'^date/(?P<date>-?\d+)/$', 'date_display', name='date_display'),
    url(r'^person/$', 'person_list_display', name='person_list_display'),
    url(r'^person/(?P<person_id>\d+)/$', 'person_display',
        name='person_display'),
    url(r'^source/$', 'source_list_display', name='source_list_display'),
    url(r'^source/(?P<source_id>\d+)/$', 'source_display',
        name='source_display'),
    url(r'^text/(?P<text_id>\d+)/$', 'text_display', name='text_display'),
)

# Search.

sqs = SearchQuerySet().facet('date').facet('person').facet('source').facet(
    'preferred_date').order_by('identifier')

urlpatterns += patterns('attribution.views',
    url(r'^text/$', search_view_factory(
        form_class=TextSearchForm, view_class=TextSearchView,
        searchqueryset=sqs,
        template='attribution/display/text_list.html'), name='text_list_display'),
)
