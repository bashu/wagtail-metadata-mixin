# -*- coding: utf-8 -*-

from django.apps import AppConfig, apps
from django.db.models.signals import post_init
from django.utils.translation import ugettext_lazy as _


def mixin(cls, mixins):
    for mixin in mixins:
        if mixin not in cls.__bases__:
            cls.__bases__ = (mixin,) + cls.__bases__
    return cls


def handle_blog_model(sender, instance, **kwargs):
    from wagtailmetadata.models import MetadataMixin

    sender = mixin(sender, [MetadataMixin])

    def get_meta_description(self):
        return self.search_description or self.description

    sender.add_to_class('get_meta_description', get_meta_description)

    def get_meta_image(self):
        if self.header_image:
            return self.build_absolute_uri(self.header_image.get_rendition('fill-800x450').url)
        return None

    sender.add_to_class('get_meta_image', get_meta_image)

    sender.object_type = "blog"

    sender._metadata = {
        'gplus_type': "Blog",
    }


class DefaultConfig(AppConfig):
    label = name = 'localsite'

    def ready(self):
        try:
            from puput.models import BlogPage

            post_init.connect(handle_blog_model, sender=BlogPage)

        except:
            pass  # shit happens
