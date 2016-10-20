# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from meta import settings as meta_settings
from meta_mixin.models import ModelMeta


class MetadataMixin(ModelMeta):
    context_meta_name = 'meta'

    _metadata_default = ModelMeta._metadata_default.copy()
    _metadata_default.update({
        'title': 'get_meta_title',
        'description': 'get_meta_description',
        'og_description': 'get_meta_description',
        'twitter_description': 'get_meta_description',
        'gplus_description': 'get_meta_description',
        'keywords': 'get_meta_keywords',
        'image': 'get_meta_image',
        # 'og_app_id': settings.FB_APPID,
        # 'og_profile_id': settings.FB_PROFILE_ID,
        # 'og_publisher': settings.FB_PUBLISHER,
        'og_author': 'get_author_name',
        'og_author_url': 'get_author_url',
        # 'fb_pages': settings.FB_PAGES,
        'twitter_type': 'get_meta_twitter_type',
        # 'twitter_site': settings.TWITTER_SITE,
        'twitter_author': 'get_author_twitter',
        # 'gplus_type': settings.GPLUS_TYPE,
        'gplus_author': 'get_author_gplus',
        # 'gplus_publisher': settings.GPLUS_PUBLISHER,
        'published_time': 'published_time',
        'modified_time': 'latest_revision_created_at',
        'expiration_time': 'expire_at',
        'url': 'full_url',
        'locale': getattr(settings, 'LANGUAGE_CODE', 'en_US'),
    })

    def get_meta_title(self):
        return self.seo_title or self.title

    def get_meta_description(self):
        return self.search_description

    def get_meta_keywords(self):
        return []

    def get_meta_image(self):
        return meta_settings.DEFAULT_IMAGE

    def get_author(self):
        author = super(MetadataMixin, self).get_author()
        author.fb_url = meta_settings.FB_AUTHOR_URL
        author.twitter_profile = meta_settings.TWITTER_AUTHOR
        author.gplus_profile = meta_settings.GPLUS_AUTHOR
        author.get_full_name = self.owner.get_full_name
        return author

    def get_meta_twitter_type(self):
        if self.get_meta_image() is not None:
            return 'summary_large_image'
        else:
            return 'summary'

    @property
    def published_time(self):
        return self.go_live_at or self.first_published_at

    def get_context(self, request):
        context = super(MetadataMixin, self).get_context(request)
        context[self.context_meta_name] = self.as_meta(request)
        return context


class MetadataPageMixin(MetadataMixin, Page):

    search_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = [
        ImageChooserPanel('search_image'),
    ]

    def get_meta_image(self):
        if self.search_image is not None:
            return self.search_image.get_rendition('original').url
        return super(MetadataPageMixin, self).get_meta_image()

    class Meta:
        abstract = True
