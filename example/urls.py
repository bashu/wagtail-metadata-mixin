import re

from django.conf import settings
from django.conf.urls import include, url

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls


urlpatterns = [
    url(r'^admin/', include(wagtailadmin_urls)),
]

if settings.SERVE_MEDIA:
    from django.views.static import serve

    urlpatterns += [
        url(r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')), serve, kwargs={
            'document_root': settings.STATIC_ROOT,
        }),
    ]

    urlpatterns += [
        url(r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL.lstrip('/')), serve, kwargs={
            'document_root': settings.MEDIA_ROOT,
        }),
    ]

urlpatterns += [
    url(r'', include('puput.urls')),
]
