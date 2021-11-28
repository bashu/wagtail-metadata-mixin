from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from meta import settings as meta_settings
from meta import utils
from meta.models import ModelMeta
from wagtail.core.models import Site
from wagtail.images import get_image_model_string
from wagtail.images.edit_handlers import ImageChooserPanel


class MetadataMixin(ModelMeta):
    context_meta_name = "meta"

    object_type = None
    schemaorg_type = None
    custom_namespace = None

    _metadata_default = {
        "use_og": "use_og",
        "use_twitter": "use_twitter",
        "use_schemaorg": "use_schemaorg",
        "use_title_tag": "use_title_tag",
        "title": "get_meta_title",
        "description": "get_meta_description",
        "keywords": "get_meta_keywords",
        "url": "get_meta_url",
        "image": "get_meta_image",
        "object_type": "get_meta_object_type",
        "site_name": "get_meta_site_name",
        "twitter_site": "get_meta_twitter_site",
        "twitter_creator": "get_meta_twitter_creator",
        "twitter_card": "get_meta_twitter_card",
        "og_author": "get_author_url",
        "og_publisher": meta_settings.FB_PUBLISHER,
        "facebook_app_id": meta_settings.FB_APPID,
        "fb_pages": meta_settings.FB_PAGES,
        "locale": "get_meta_locale",
        "schemaorg_type": "get_meta_schemaorg_type",
        "custom_namespace": "get_meta_custom_namespace",
        "get_domain": "get_domain",
    }

    @property
    def use_og(self):
        return meta_settings.USE_OG_PROPERTIES

    @property
    def use_twitter(self):
        return meta_settings.USE_TWITTER_PROPERTIES

    @property
    def use_schemaorg(self):
        return meta_settings.USE_SCHEMAORG_PROPERTIES

    @property
    def use_title_tag(self):
        return meta_settings.USE_TITLE_TAG

    def get_meta_title(self):
        return False

    def get_meta_description(self):
        return False

    def get_meta_keywords(self):
        return []

    def get_meta_url(self):
        return False

    def get_meta_image(self):
        if bool(meta_settings.DEFAULT_IMAGE) is True:
            return self.build_absolute_uri(meta_settings.DEFAULT_IMAGE)
        return None

    def get_meta_object_type(self):
        return self.object_type or meta_settings.SITE_TYPE

    def get_meta_schemaorg_type(self):
        return self.schemaorg_type or meta_settings.SCHEMAORG_TYPE

    def get_meta_site_name(self):
        request = utils.get_request()
        site = getattr(request, "site", None)
        if request and isinstance(site, Site):
            if bool(request.site.site_name) is True:
                return request.site.site_name

        site = self.get_site()
        if isinstance(site, Site):
            if bool(site.site_name) is True:
                return site.site_name

        if request:
            site = Site.find_for_request(request)
            if isinstance(site, Site):
                return site.site_name

        return settings.WAGTAIL_SITE_NAME

    def get_meta_twitter_site(self):
        return meta_settings.TWITTER_SITE

    def get_meta_twitter_creator(self):
        return self.get_author_twitter()

    def get_meta_twitter_card(self):
        if self.get_meta_image() is not None:
            return "summary_large_image"
        return "summary"

    def get_meta_locale(self):
        return getattr(settings, "LANGUAGE_CODE", "en_US")

    def get_meta_custom_namespace(self):
        return self.custom_namespace or meta_settings.OG_NAMESPACES

    def get_domain(self):
        request = utils.get_request()
        if request and getattr(request, "site", None):
            return request.site.hostname

        site = self.get_site()
        if site is not None:
            if bool(site.hostname) is True:
                return site.hostname

        if not meta_settings.SITE_DOMAIN:
            raise ImproperlyConfigured("META_SITE_DOMAIN is not set")

        return meta_settings.SITE_DOMAIN

    def get_author(self):
        class Author:
            fb_url = meta_settings.FB_AUTHOR_URL
            twitter_profile = meta_settings.TWITTER_AUTHOR
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
            return "{}{}".format(site.root_url, url if url.startswith("/") else "/" + url)

        raise NotImplementedError

    def get_context(self, request):
        context = super().get_context(request)
        context[self.context_meta_name] = self.as_meta(request)
        return context


class MetadataPageMixin(MetadataMixin, models.Model):

    search_image = models.ForeignKey(
        get_image_model_string(), null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    panels = [ImageChooserPanel("search_image")]

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
                self.search_image.get_rendition(getattr(settings, "META_SEARCH_IMAGE_RENDITION", "fill-800x450")).url
            )
        return super().get_meta_image()

    def get_author(self):
        author = super().get_author()
        if hasattr(self, "owner") and isinstance(self.owner, get_user_model()):
            author.get_full_name = self.owner.get_full_name
        return author
