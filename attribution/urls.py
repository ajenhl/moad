from django.conf.urls import patterns, url

urlpatterns = patterns('attribution.views',
    url(r'^$', 'home_display', name='home_display'),
    url(r'^person/$', 'person_list_display', name='person_list_display'),
    url(r'^person/(?P<person_id>\d+)/$', 'person_display',
        name='person_display'),
    url(r'^source/$', 'source_list_display', name='source_list_display'),
    url(r'^source/(?P<source_id>\d+)/$', 'source_display',
        name='source_display'),
    url(r'^text/$', 'text_list_display', name='text_list_display'),
    url(r'^text/(?P<text_id>\d+)/$', 'text_display', name='text_display'),
)
