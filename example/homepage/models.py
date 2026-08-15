from django.utils.html import strip_tags
from django.utils.text import Truncator

from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page

from wagtailmetadata.models import MetadataPageMixin


class HomePage(MetadataPageMixin, Page):
    promote_panels = Page.promote_panels + MetadataPageMixin.panels


class ArticlePage(MetadataPageMixin, Page):
    object_type = "article"
    schemaorg_type = "Article"

    body = RichTextField(blank=True)

    content_panels = [*Page.content_panels, FieldPanel("body")]
    promote_panels = Page.promote_panels + MetadataPageMixin.panels

    def get_meta_description(self):
        return self.search_description or Truncator(strip_tags(self.body)).words(20)
