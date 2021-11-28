from django.conf import settings
from django.template.defaultfilters import truncatewords
from django.urls import reverse
from django.utils.html import strip_tags

from puput import abstracts as puput
from wagtailmetadata.models import MetadataMixin


class EntryAbstract(MetadataMixin, puput.EntryAbstract):
    object_type = "article"
    schemaorg_type = "blog"

    _metadata = {
        "published_time": "date",
        "modified_time": "latest_revision_created_at",
        "expiration_time": "expire_at",
        "tag": "get_tags",
    }

    class Meta:
        abstract = True

    def get_meta_title(self):
        return self.seo_title or self.title

    def get_meta_description(self):
        return strip_tags(self.excerpt) or truncatewords(strip_tags(self.body), 20)

    def get_meta_keywords(self):
        return []

    def get_meta_url(self):
        return self.build_absolute_uri(
            reverse(
                "entry_page_serve_slug",
                kwargs={
                    "blog_path": self.blog_page.slug,
                    "year": self.date.strftime("%Y"),
                    "month": self.date.strftime("%m"),
                    "day": self.date.strftime("%d"),
                    "slug": self.slug,
                },
            )
        )

    def get_meta_image(self):
        if self.header_image is not None:
            return self.build_absolute_uri(
                self.header_image.get_rendition(getattr(settings, "META_SEARCH_IMAGE_RENDITION", "fill-800x450")).url
            )
        return None

    def get_author(self):
        author = super().get_author()
        author.get_full_name = self.owner.get_full_name
        return author

    def get_tags(self):
        return ",".join(self.tags.values_list("name", flat=True))
