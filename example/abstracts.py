# -*- coding: utf-8 -*-

from django.urls import reverse
from django.utils.html import strip_tags
from django.template.defaultfilters import truncatewords

from wagtailmetadata.models import MetadataMixin

from puput import abstracts as puput


class EntryAbstract(MetadataMixin, puput.EntryAbstract):
    object_type = 'article'

    class Meta:
        abstract = True

    def get_meta_description(self):
        return self.search_description or truncatewords(strip_tags(self.body), 20)

    def get_meta_image(self):
        if self.header_image:
            return self.build_absolute_uri(self.header_image.get_rendition('fill-800x450').url)
        return None

    def get_meta_url(self):
        return self.build_absolute_uri(
            reverse('entry_page_serve_slug', kwargs={
                'blog_path': self.blog_page.slug,
                'year': self.date.strftime('%Y'),
                'month': self.date.strftime('%m'),
                'day': self.date.strftime('%d'),
                'slug': self.slug
            })
        )
