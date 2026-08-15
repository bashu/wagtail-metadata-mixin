from django.conf import settings
from django.test import TestCase
from django.utils import timezone

from wagtail.images.models import Image
from wagtail.images.tests.utils import get_test_image_file
from wagtail.models import Site

from wagtailmetadata.tests.models import SimplePage


class TestMetadataPageMixin(TestCase):
    def setUp(self):
        self.site = Site.objects.first()
        self.site.site_name = "Example"
        self.site.hostname = "example.com"
        self.site.save()

        self.image = Image.objects.create(title="Image", file=get_test_image_file())

        self.page = self.site.root_page.add_child(
            instance=SimplePage(title="Simple Page"),
        )

    def test_published_time(self):
        assert self.page.published_time == self.page.first_published_at

        self.page.go_live_at = timezone.now()

        assert self.page.published_time == self.page.go_live_at

    def test_get_meta_title(self):
        assert self.page.get_meta_title() == "Simple Page"

        self.page.seo_title = "Lorem ipsum..."

        assert self.page.get_meta_title() == "Lorem ipsum..."

    def test_get_meta_description(self):
        assert self.page.get_meta_description() == ""

        self.page.search_description = "Lorem ipsum dolor sit amet..."

        assert self.page.get_meta_description() == "Lorem ipsum dolor sit amet..."

    def test_get_meta_keywords(self):
        assert self.page.get_meta_keywords() == []

    def test_get_meta_url(self):
        assert self.page.get_meta_url() == self.page.build_absolute_uri("/simple-page/")

    def test_get_meta_image(self):
        assert self.page.get_meta_image() is None

        self.page.search_image = self.image

        assert self.page.get_meta_image() == self.page.build_absolute_uri(
            self.image.get_rendition("fill-800x450").url,
        )

    def test_get_meta_image_with_settings(self):
        assert self.page.get_meta_image() is None

        with self.settings(META_DEFAULT_IMAGE="image.png"):
            assert self.page.get_meta_image() == self.page.build_absolute_uri(
                "image.png",
            )

    def test_get_meta_object_type(self):
        assert self.page.get_meta_object_type() is None

        self.page.object_type = "article"

        assert self.page.get_meta_object_type() == "article"

    def test_get_meta_site_name(self):
        assert self.page.get_meta_site_name() == "Example"

        self.site.site_name = "Site Name"
        self.site.save()

        assert self.page.get_meta_site_name() == "Site Name"

    def test_get_meta_site_name_with_settings(self):
        assert self.page.get_meta_site_name() == "Example"

        self.site.site_name = ""  # for testing purpose
        self.site.save()

        with self.settings(WAGTAIL_SITE_NAME="Site Name"):
            assert self.page.get_meta_site_name() == "Site Name"

    def test_get_meta_twitter_site(self):
        assert self.page.get_meta_twitter_site() == ""

        with self.settings(META_TWITTER_SITE="@site"):
            assert self.page.get_meta_twitter_site() == "@site"

    def test_get_meta_twitter_creator(self):
        assert self.page.get_meta_twitter_creator() == ""

        with self.settings(META_TWITTER_AUTHOR="@author"):
            assert self.page.get_meta_twitter_creator() == "@author"

    def test_get_meta_twitter_card(self):
        assert self.page.get_meta_twitter_card() == "summary"

        self.page.search_image = self.image

        assert self.page.get_meta_twitter_card() == "summary_large_image"

    def test_get_meta_locale(self):
        assert self.page.get_meta_locale() == getattr(
            settings,
            "LANGUAGE_CODE",
            "en_US",
        )

        with self.settings(LANGUAGE_CODE="ru_RU"):
            assert self.page.get_meta_locale() == "ru_RU"

    def test_get_meta_schemaorg_type(self):
        assert self.page.get_meta_schemaorg_type() == "Article"

        self.page.schemaorg_type = "Page"

        assert self.page.get_meta_schemaorg_type() == "Page"

    def test_get_meta_custom_namespace(self):
        assert self.page.get_meta_custom_namespace() is None

        self.page.custom_namespace = "website"

        assert self.page.get_meta_custom_namespace() == "website"

    def test_get_meta_custom_namespace_with_settings(self):
        assert self.page.get_meta_custom_namespace() is None

        with self.settings(META_OG_NAMESPACES=["foo", "bar"]):
            assert self.page.get_meta_custom_namespace() == ["foo", "bar"]

    def test_get_domain(self):
        assert self.page.get_domain() == "example.com"

        self.site.hostname = "domain.com"
        self.site.save()

        assert self.page.get_domain() == "domain.com"
