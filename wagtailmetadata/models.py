# -*- coding: utf-8 -*-

from django.conf import settings

from meta_mixin.models import ModelMeta


class MetadataPageMixin(ModelMeta):
    context_meta_name = 'meta'

    _metadata_default = ModelMeta._metadata_default.copy()
    _metadata_default.update({
        'title': 'get_meta_title',
        'description': 'get_meta_description',
        'og_description': 'get_meta_description',
        'twitter_description': 'get_meta_description',
        'gplus_description': 'get_meta_description',
        'keywords': 'get_meta_keywords',
        # 'image': 'search_image',
        # 'og_app_id': settings.FB_APPID,
        # 'og_profile_id': settings.FB_PROFILE_ID,
        # 'og_publisher': settings.FB_PUBLISHER,
        # 'fb_pages': settings.FB_PAGES,
        # 'twitter_type': settings.TWITTER_TYPE,
        # 'twitter_site': settings.TWITTER_SITE,
        # 'gplus_type': settings.GPLUS_TYPE,
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

    def get_author(self):
        author = super(ModelMeta, self).get_author()
        author.get_full_name = self.owner.get_full_name
        return author

    @property
    def published_time(self):
        return self.go_live_at or self.first_published_at

    def get_context(self, request):
        context = super(MetadataPageMixin, self).get_context(request)
        context[self.context_meta_name] = self.as_meta(request)
        return context
