import re

from django.conf import settings
from django.conf.urls import include, url
from django.urls import path

urlpatterns = []

if settings.SERVE_MEDIA:
    from django.views.static import serve

    urlpatterns += [
        url(
            r"^%s(?P<path>.*)$" % re.escape(settings.STATIC_URL.lstrip("/")),
            serve,
            kwargs={"document_root": settings.STATIC_ROOT},
        )
    ]

    urlpatterns += [
        url(
            r"^%s(?P<path>.*)$" % re.escape(settings.MEDIA_URL.lstrip("/")),
            serve,
            kwargs={"document_root": settings.MEDIA_ROOT},
        )
    ]

urlpatterns += [path(r"", include("puput.urls"))]
