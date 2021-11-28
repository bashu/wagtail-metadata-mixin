from wagtail.core.models import Page

from wagtailmetadata.models import MetadataPageMixin


class SimplePage(MetadataPageMixin, Page):
    promote_panels = Page.promote_panels + MetadataPageMixin.panels
