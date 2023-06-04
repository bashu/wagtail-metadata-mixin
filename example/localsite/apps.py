from django.apps import AppConfig
from django.db.models.signals import post_init
from django.template.defaultfilters import truncatewords


def add_mixins(cls, mixins):
    for mixin in mixins:
        if mixin not in cls.__bases__:
            cls.__bases__ = (mixin,) + cls.__bases__
    return cls


def handle_blog_model(sender, instance, **kwargs):
    from wagtailmetadata.models import MetadataMixin

    sender = add_mixins(sender, [MetadataMixin])

    def get_meta_description(cls):
        return cls.search_description or truncatewords(cls.description, 20)

    sender.add_to_class("get_meta_description", get_meta_description)

    def get_meta_image(cls):
        if cls.header_image is not None:
            return cls.build_absolute_uri(cls.header_image.get_rendition("fill-800x450").url)
        return super(sender, cls).get_meta_image()

    sender.add_to_class("get_meta_image", get_meta_image)

    sender.object_type = "blog"

    sender._metadata = {"gplus_type": "Blog"}


class DefaultConfig(AppConfig):
    label = name = "localsite"

    def ready(self):
        try:
            from puput.models import BlogPage

            post_init.connect(handle_blog_model, sender=BlogPage)

        except:  # noqa
            pass  # shit happens
