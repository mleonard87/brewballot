from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'brewballot.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'poll.views.poll_default'),

    url(r'^poll/', include('poll.urls')),

    url(r'^all/$', 'poll.views.poll_all', name='poll_all'),

    url(r'^admin/', include(admin.site.urls)),
)

# Uncomment the next line to serve media files in dev.
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
