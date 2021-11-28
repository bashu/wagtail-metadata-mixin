import re

from django.conf import settings
from django.urls import include, path, re_path

urlpatterns = []

if settings.SERVE_MEDIA:
    from django.views.static import serve

    urlpatterns += [
        re_path(
            r"^%s(?P<path>.*)$" % re.escape(settings.STATIC_URL.lstrip("/")),
            serve,
            kwargs={"document_root": settings.STATIC_ROOT},
        )
    ]

    urlpatterns += [
        re_path(
            r"^%s(?P<path>.*)$" % re.escape(settings.MEDIA_URL.lstrip("/")),
            serve,
            kwargs={"document_root": settings.MEDIA_ROOT},
        )
    ]

urlpatterns += [path(r"", include("puput.urls"))]
