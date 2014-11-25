from django.conf.urls import patterns, url

urlpatterns = patterns('poll.views',
    url(r'^(?P<poll_id>[0-9]*)/(?P<poll_slug>[a-z0-9\-]*)/$', 'poll_results', name='poll_results'),
)