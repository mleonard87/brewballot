from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('poll.views',
    url(r'^(?P<poll_id>[0-9]*)/(?P<poll_slug>[a-z0-9\-]*)/$', 'poll_results', name='poll_results'),
    url(r'^sms$', 'sms_inbound'),
    url(r'^no-active-polls/$', TemplateView.as_view(template_name='poll/no_active_polls.html'), name='no_active_polls')
)