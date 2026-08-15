from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.translation import gettext_lazy as _

from meta import utils
from meta.models import ModelMeta
from meta.settings import get_setting
from wagtail.admin.panels import FieldPanel
from wagtail.images import get_image_model_string
from wagtail.models import Site


class MetadataMixin(ModelMeta):
    context_meta_name = "meta"

    og_type = None
    object_type = None
    schemaorg_type = None
    custom_namespace = None

    _metadata_default = {
        "use_og": "use_og",
        "use_twitter": "use_twitter",
        "use_schemaorg": "use_schemaorg",
        "use_json_ld": "use_json_ld",
        "use_title_tag": "use_title_tag",
        "title": "get_meta_title",
        "og_title": "get_meta_og_title",
        "twitter_title": "get_meta_twitter_title",
        "schemaorg_title": "get_meta_schemaorg_title",
        "description": "get_meta_description",
        "og_description": "get_meta_og_description",
        "twitter_description": "get_meta_twitter_description",
        "schemaorg_description": "get_meta_schemaorg_description",
        "keywords": "get_meta_keywords",
        "url": "get_meta_url",
        "image": "get_meta_image",
        "image_width": "get_meta_image_width",
        "image_height": "get_meta_image_height",
        "object_type": "get_meta_object_type",
        "site_name": "get_meta_site_name",
        "og_type": "get_meta_og_type",
        "og_app_id": "get_meta_og_app_id",
        "og_profile_id": "get_meta_og_profile_id",
        "og_publisher": "get_meta_og_publisher",
        "og_author_url": "get_meta_og_author_url",
        "fb_pages": get_setting("FB_PAGES"),
        "twitter_site": "get_meta_twitter_site",
        "twitter_creator": "get_meta_twitter_creator",
        "twitter_type": "get_meta_twitter_type",
        "schemaorg_type": "get_meta_schemaorg_type",
        "locale": "get_meta_locale",
        "custom_namespace": "get_meta_custom_namespace",
        "get_domain": "get_domain",
    }

    @property
    def use_og(self):
        return get_setting("USE_OG_PROPERTIES")

    @property
    def use_twitter(self):
        return get_setting("USE_TWITTER_PROPERTIES")

    @property
    def use_schemaorg(self):
        return get_setting("USE_SCHEMAORG_PROPERTIES")

    @property
    def use_json_ld(self):
        return get_setting("USE_JSON_LD_SCHEMA")

    @property
    def use_title_tag(self):
        return get_setting("USE_TITLE_TAG")

    def get_meta_title(self):
        return False

    def get_meta_og_title(self):
        return False

    def get_meta_twitter_title(self):
        return False

    def get_meta_schemaorg_title(self):
        return False

    def get_meta_description(self):
        return False

    def get_meta_og_description(self):
        return False

    def get_meta_twitter_description(self):
        return False

    def get_meta_schemaorg_description(self):
        return False

    def get_meta_keywords(self):
        return []

    def get_meta_url(self):
        return False

    def get_meta_image(self):
        if bool(get_setting("DEFAULT_IMAGE")) is True:
            return self.build_absolute_uri(get_setting("DEFAULT_IMAGE"))
        return None

    def get_meta_image_width(self):
        return None

    def get_meta_image_height(self):
        return None

    def get_meta_object_type(self):
        return self.object_type or get_setting("DEFAULT_TYPE")

    def get_meta_schemaorg_type(self):
        return self.schemaorg_type or get_setting("SCHEMAORG_TYPE")

    def get_meta_site_name(self):
        request = utils.get_request()
        if request:
            site = Site.find_for_request(request)
            if isinstance(site, Site):
                return site.site_name

        site = self.get_site()
        if isinstance(site, Site):
            if bool(site.site_name) is True:
                return site.site_name

        return settings.WAGTAIL_SITE_NAME

    def get_meta_og_type(self):
        return self.og_type or get_setting("FB_TYPE")

    def get_meta_og_app_id(self):
        return get_setting("FB_APPID")

    def get_meta_og_profile_id(self):
        return get_setting("FB_PROFILE_ID")

    def get_meta_og_publisher(self):
        return get_setting("FB_PUBLISHER")

    def get_meta_og_author_url(self):
        return self.get_author_url()

    def get_meta_twitter_site(self):
        return get_setting("TWITTER_SITE")

    def get_meta_twitter_creator(self):
        return self.get_author_twitter()

    def get_meta_twitter_type(self):
        if self.get_meta_image() is not None:
            return "summary_large_image"
        return "summary"

    def get_meta_locale(self):
        return getattr(settings, "LANGUAGE_CODE", "en_US")

    def get_meta_custom_namespace(self):
        return self.custom_namespace or get_setting("OG_NAMESPACES")

    def get_domain(self):
        request = utils.get_request()
        if request:
            site = Site.find_for_request(request)
            if isinstance(site, Site):
                return site.hostname

        site = self.get_site()
        if isinstance(site, Site):
            if bool(site.hostname) is True:
                return site.hostname

        if not get_setting("SITE_DOMAIN"):
            msg = "META_SITE_DOMAIN is not set"
            raise ImproperlyConfigured(msg)

        return get_setting("SITE_DOMAIN")

    def get_author(self):
        class Author:
            fb_url = get_setting("FB_AUTHOR_URL")
            twitter_profile = get_setting("TWITTER_AUTHOR")
            schemaorg_profile = None

            def get_full_name(self):  # pragma: no cover
                return None

        return Author()

    def build_absolute_uri(self, url):
        request = utils.get_request()
        if request is not None:
            return request.build_absolute_uri(url)

        if url.startswith("http"):
            return url

        site = self.get_site()
        if site is not None:
            return "{}{}".format(
                site.root_url,
                url if url.startswith("/") else "/" + url,
            )

        raise NotImplementedError

    def get_context(self, request):
        context = super().get_context(request)
        context[self.context_meta_name] = self.as_meta(request)
        return context


class MetadataPageMixin(MetadataMixin, models.Model):
    search_image = models.ForeignKey(
        get_image_model_string(),
        verbose_name=_("search image"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [FieldPanel("search_image")]

    _metadata = {
        "published_time": "published_time",
        "modified_time": "latest_revision_created_at",
        "expiration_time": "expire_at",
    }

    class Meta:
        abstract = True

    @property
    def published_time(self):
        return self.go_live_at or self.first_published_at

    def get_meta_title(self):
        return self.seo_title or self.title

    def get_meta_description(self):
        return self.search_description

    def get_meta_keywords(self):
        return []

    def get_meta_url(self):
        return self.build_absolute_uri(self.url)

    def get_meta_image(self):
        if self.search_image is not None:
            return self.build_absolute_uri(
                self.search_image.get_rendition(
                    getattr(settings, "META_SEARCH_IMAGE_RENDITION", "fill-800x450"),
                ).url,
            )
        return super().get_meta_image()

    def get_meta_image_width(self):
        if self.search_image is not None:
            rendition = self.search_image.get_rendition(
                getattr(settings, "META_SEARCH_IMAGE_RENDITION", "fill-800x450"),
            )
            return rendition.width
        return super().get_meta_image_width()

    def get_meta_image_height(self):
        if self.search_image is not None:
            rendition = self.search_image.get_rendition(
                getattr(settings, "META_SEARCH_IMAGE_RENDITION", "fill-800x450"),
            )
            return rendition.height
        return super().get_meta_image_height()

    def get_author(self):
        author = super().get_author()
        if hasattr(self, "owner") and isinstance(self.owner, get_user_model()):
            author.get_full_name = self.owner.get_full_name
        return author
