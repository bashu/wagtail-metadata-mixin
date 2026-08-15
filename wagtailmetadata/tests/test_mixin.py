from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django.utils import timezone

import pytest
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

    def test_use_og(self):
        assert self.page.use_og is True

        with self.settings(META_USE_OG_PROPERTIES=False):
            assert self.page.use_og is False

    def test_use_twitter(self):
        assert self.page.use_twitter is True

        with self.settings(META_USE_TWITTER_PROPERTIES=False):
            assert self.page.use_twitter is False

    def test_use_schemaorg(self):
        assert self.page.use_schemaorg is True

        with self.settings(META_USE_SCHEMAORG_PROPERTIES=False):
            assert self.page.use_schemaorg is False

    def test_use_json_ld(self):
        assert self.page.use_json_ld is True

        with self.settings(META_USE_JSON_LD_SCHEMA=False):
            assert self.page.use_json_ld is False

    def test_use_title_tag(self):
        assert self.page.use_title_tag is False

        with self.settings(META_USE_TITLE_TAG=True):
            assert self.page.use_title_tag is True

    def test_get_meta_title(self):
        assert self.page.get_meta_title() == "Simple Page"

        self.page.seo_title = "Lorem ipsum..."

        assert self.page.get_meta_title() == "Lorem ipsum..."

    def test_get_meta_og_title(self):
        assert self.page.get_meta_og_title() is False

    def test_get_meta_twitter_title(self):
        assert self.page.get_meta_twitter_title() is False

    def test_get_meta_schemaorg_title(self):
        assert self.page.get_meta_schemaorg_title() is False

    def test_get_meta_description(self):
        assert self.page.get_meta_description() == ""

        self.page.search_description = "Lorem ipsum dolor sit amet..."

        assert self.page.get_meta_description() == "Lorem ipsum dolor sit amet..."

    def test_get_meta_og_description(self):
        assert self.page.get_meta_og_description() is False

    def test_get_meta_twitter_description(self):
        assert self.page.get_meta_twitter_description() is False

    def test_get_meta_schemaorg_description(self):
        assert self.page.get_meta_schemaorg_description() is False

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
        assert self.page.get_meta_object_type() == "Article"

        self.page.object_type = "Website"

        assert self.page.get_meta_object_type() == "Website"

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

    def test_get_meta_twitter_type(self):
        assert self.page.get_meta_twitter_type() == "summary"

        self.page.search_image = self.image

        assert self.page.get_meta_twitter_type() == "summary_large_image"

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

    def test_get_domain_without_site_raises(self):
        self.site.delete()

        with pytest.raises(ImproperlyConfigured):
            self.page.get_domain()

    def test_get_domain_without_site_with_settings(self):
        self.site.delete()

        with self.settings(META_SITE_DOMAIN="example.org"):
            assert self.page.get_domain() == "example.org"

    def test_get_meta_image_width(self):
        assert self.page.get_meta_image_width() is None

        self.page.search_image = self.image

        rendition = self.image.get_rendition("fill-800x450")
        assert self.page.get_meta_image_width() == rendition.width

    def test_get_meta_image_height(self):
        assert self.page.get_meta_image_height() is None

        self.page.search_image = self.image

        rendition = self.image.get_rendition("fill-800x450")
        assert self.page.get_meta_image_height() == rendition.height

    def test_get_meta_og_type(self):
        assert self.page.get_meta_og_type() == "Article"

        self.page.og_type = "website"

        assert self.page.get_meta_og_type() == "website"

    def test_get_meta_og_app_id(self):
        assert self.page.get_meta_og_app_id() == ""

        with self.settings(META_FB_APPID="12345"):
            assert self.page.get_meta_og_app_id() == "12345"

    def test_get_meta_og_profile_id(self):
        assert self.page.get_meta_og_profile_id() == ""

        with self.settings(META_FB_PROFILE_ID="profile"):
            assert self.page.get_meta_og_profile_id() == "profile"

    def test_get_meta_og_publisher(self):
        assert self.page.get_meta_og_publisher() == ""

        with self.settings(META_FB_PUBLISHER="https://facebook.com/foo"):
            assert self.page.get_meta_og_publisher() == "https://facebook.com/foo"

    def test_get_meta_og_author_url(self):
        assert self.page.get_meta_og_author_url() == self.page.get_author_url()

    def test_get_author(self):
        author = self.page.get_author()

        assert author.get_full_name() is None

    def test_get_author_with_owner(self):
        user = get_user_model().objects.create(
            username="author",
            first_name="Jane",
            last_name="Doe",
        )
        self.page.owner = user

        author = self.page.get_author()

        assert author.get_full_name() == "Jane Doe"

    def test_build_absolute_uri_with_absolute_url(self):
        assert (
            self.page.build_absolute_uri("http://external.example/")
            == "http://external.example/"
        )

    def test_build_absolute_uri_without_site_raises(self):
        self.site.delete()

        with pytest.raises(NotImplementedError):
            self.page.build_absolute_uri("/foo/")
