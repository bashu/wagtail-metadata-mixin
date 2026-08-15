from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.static import serve

from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("dashboard/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path(
        "media/<path:path>",
        serve,
        kwargs={"document_root": settings.MEDIA_ROOT},
    ),
    path("", include(wagtail_urls)),
]
