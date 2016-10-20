from django.db import models
from django.utils import six

from wagtail.wagtailcore.models import Page as BasePage

from wagtailmetadata.models import MetadataMixin, MetadataPageMixin


class PageBase(type(BasePage)):
    pass


class Page(six.with_metaclass(PageBase, MetadataPageMixin, BasePage)):

    promote_panels = BasePage.promote_panels + MetadataPageMixin.panels
