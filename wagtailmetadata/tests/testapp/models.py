# -*- coding: utf-8 -*-

from django.utils import six

from wagtail.core.models import Page, PageBase

from wagtailmetadata.models import MetadataMixin, MetadataPageMixin


class SimplePage(six.with_metaclass(PageBase, MetadataPageMixin, Page)):
    promote_panels = Page.promote_panels + MetadataPageMixin.panels

