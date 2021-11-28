from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from meta import settings as meta_settings
from wagtail.core.models import Site
from wagtail.images.models import Image
from wagtail.images.tests.utils import get_test_image_file

from wagtailmetadata.tests.models import SimplePage


class TestMetadataPageMixin(TestCase):
    def setUp(self):
        self.site = Site.objects.first()
        self.site.site_name = "Example"
        self.site.hostname = "example.com"
        self.site.save()

        self.image = Image.objects.create(title="Image", file=get_test_image_file())

        self.page = self.site.root_page.add_child(instance=SimplePage(title="Simple Page"))

    def test_published_time(self):
        self.assertEqual(self.page.published_time, self.page.first_published_at)

        self.page.go_live_at = timezone.now()

        self.assertEqual(self.page.published_time, self.page.go_live_at)

    def test_get_meta_title(self):
        self.assertEqual(self.page.get_meta_title(), "Simple Page")

        self.page.seo_title = "Lorem ipsum..."

        self.assertEqual(self.page.get_meta_title(), "Lorem ipsum...")

    def test_get_meta_description(self):
        self.assertEqual(self.page.get_meta_description(), "")

        self.page.search_description = "Lorem ipsum dolor sit amet..."

        self.assertEqual(self.page.get_meta_description(), "Lorem ipsum dolor sit amet...")

    def test_get_meta_keywords(self):
        self.assertEqual(self.page.get_meta_keywords(), [])

    def test_get_meta_url(self):
        self.assertEqual(self.page.get_meta_url(), self.page.build_absolute_uri("/simple-page/"))

    def test_get_meta_image(self):
        self.assertEqual(self.page.get_meta_image(), None)

        self.page.search_image = self.image

        self.assertEqual(
            self.page.get_meta_image(), self.page.build_absolute_uri(self.image.get_rendition("fill-800x450").url)
        )

    def test_get_meta_image_with_settings(self):
        self.assertEqual(self.page.get_meta_image(), None)

        old_DEFAULT_IMAGE = meta_settings.DEFAULT_IMAGE
        meta_settings.DEFAULT_IMAGE = "image.png"

        self.assertEqual(self.page.get_meta_image(), self.page.build_absolute_uri("image.png"))

        meta_settings.DEFAULT_IMAGE = old_DEFAULT_IMAGE

    def test_get_meta_object_type(self):
        self.assertEqual(self.page.get_meta_object_type(), None)

        self.page.object_type = "article"

        self.assertEqual(self.page.get_meta_object_type(), "article")

    def test_get_meta_site_name(self):
        self.assertEqual(self.page.get_meta_site_name(), "Example")

        self.site.site_name = "Site Name"
        self.site.save()

        self.assertEqual(self.page.get_meta_site_name(), "Site Name")

    def test_get_meta_site_name_with_settings(self):
        self.assertEqual(self.page.get_meta_site_name(), "Example")

        self.site.site_name = ""  # for testing purpose
        self.site.save()

        with self.settings(WAGTAIL_SITE_NAME="Site Name"):
            self.assertEqual(self.page.get_meta_site_name(), "Site Name")

    def test_get_meta_twitter_site(self):
        self.assertEqual(self.page.get_meta_twitter_site(), "")

        old_TWITTER_SITE = meta_settings.TWITTER_SITE
        meta_settings.TWITTER_SITE = "@site"

        self.assertEqual(self.page.get_meta_twitter_site(), "@site")

        meta_settings.TWITTER_SITE = old_TWITTER_SITE

    def test_get_meta_twitter_creator(self):
        self.assertEqual(self.page.get_meta_twitter_creator(), "")

        old_TWITTER_AUTHOR = meta_settings.TWITTER_AUTHOR
        meta_settings.TWITTER_AUTHOR = "@author"

        self.assertEqual(self.page.get_meta_twitter_creator(), "@author")

        meta_settings.TWITTER_AUTHOR = old_TWITTER_AUTHOR

    def test_get_meta_twitter_card(self):
        self.assertEqual(self.page.get_meta_twitter_card(), "summary")

        self.page.search_image = self.image

        self.assertEqual(self.page.get_meta_twitter_card(), "summary_large_image")

    def test_get_meta_locale(self):
        self.assertEqual(self.page.get_meta_locale(), getattr(settings, "LANGUAGE_CODE", "en_US"))

        with self.settings(LANGUAGE_CODE="ru_RU"):
            self.assertEqual(self.page.get_meta_locale(), "ru_RU")

    def test_get_meta_schemaorg_type(self):
        self.assertEqual(self.page.get_meta_schemaorg_type(), "Article")

        self.page.schemaorg_type = "Page"

        self.assertEqual(self.page.get_meta_schemaorg_type(), "Page")

    def test_get_meta_custom_namespace(self):
        self.assertEqual(self.page.get_meta_custom_namespace(), None)

        self.page.custom_namespace = "website"

        self.assertEqual(self.page.get_meta_custom_namespace(), "website")

    def test_get_meta_custom_namespace_with_settings(self):
        self.assertEqual(self.page.get_meta_custom_namespace(), None)

        old_OG_NAMESPACES = meta_settings.OG_NAMESPACES
        meta_settings.OG_NAMESPACES = ["foo", "bar"]

        self.assertEqual(self.page.get_meta_custom_namespace(), ["foo", "bar"])

        meta_settings.OG_NAMESPACES = old_OG_NAMESPACES

    def test_get_domain(self):
        self.assertEqual(self.page.get_domain(), "example.com")

        self.site.hostname = "domain.com"
        self.site.save()

        self.assertEqual(self.page.get_domain(), "domain.com")
