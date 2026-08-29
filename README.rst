wagtail-metadata-mixin
======================

.. image:: https://badge.fury.io/py/wagtail-metadata-mixin.svg
    :target: https://badge.fury.io/py/wagtail-metadata-mixin

.. image:: https://img.shields.io/pypi/pyversions/wagtail-metadata-mixin.svg
    :target: https://pypi.python.org/pypi/wagtail-metadata-mixin/

.. image:: https://img.shields.io/pypi/djversions/wagtail-metadata-mixin.svg
    :target: https://pypi.python.org/pypi/wagtail-metadata-mixin/

.. image:: https://github.com/bashu/wagtail-metadata-mixin/actions/workflows/test.yml/badge.svg
    :target: https://github.com/bashu/wagtail-metadata-mixin/actions/workflows/test.yml

OpenGraph, Twitter Card and Schema.org snippet tags for Wagtail CMS pages.

The current version is tested for compatiblily with the following:

- Wagtail versions 6.3 to 8.0
- Django versions 5.2, 6.0 and 6.1
- Python versions 3.10 to 3.14

Authored by `Basil Shubin <https://github.com/bashu>`_,  and some great
`contributors <https://github.com/bashu/wagtail-metadata-mixin/contributors>`_.

Installation
------------

First install the module, preferably in a virtual environment. It can be installed from PyPI:

.. code-block:: shell

    pip install wagtail-metadata-mixin

Requirements
~~~~~~~~~~~~

You must have *django-meta* installed and configured, see the
django-meta_ documentation for details and setup instructions.

Setup
-----

First make sure the project is configured for django-meta_.

Then add the following settings:

.. code-block:: python

    INSTALLED_APPS += (
        'wagtailmetadata',
    )

and just include ``meta/meta.html`` template in your templates

.. code-block:: html+django

    {% load meta %}

    <html {% meta_namespaces_schemaorg %}>
        <head {% meta_namespaces %}>
            {% include "meta/meta.html" %}
        </head>
        <body>...</body>
    </html>

Check django-meta_ documentation for more details.

Usage
-----

.. code-block:: python

    # models.py

    from wagtail.models import Page, PageBase

    from wagtailmetadata.models import MetadataPageMixin

    # ensure MetadataPageMixin class goes before Page class
    class CustomPage(MetadataPageMixin, Page):
        schemaorg_type = "Page"

        promote_panels = Page.promote_panels + MetadataPageMixin.panels


``MetadataPageMixin`` already provides sensible defaults for every field (``title`` uses
``seo_title`` or ``title``, ``description`` uses ``search_description``, ``image`` uses
``search_image``, and so on). There are two ways to customise them on your own page.

Overriding the ``get_meta_*`` methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The most common approach -- override the relevant method(s), the same way
``MetadataPageMixin`` itself overrides ``MetadataMixin``:

.. code-block:: python

    class ArticlePage(MetadataPageMixin, Page):
        body = RichTextField(blank=True)

        def get_meta_description(self):
            return self.search_description or Truncator(strip_tags(self.body)).words(30)

        def get_meta_twitter_type(self):
            return "summary_large_image"

Overriding ``_metadata``
~~~~~~~~~~~~~~~~~~~~~~~~

If you just want to point an existing field at a different attribute or method, without
writing a whole new ``get_meta_*`` method, extend ``_metadata`` instead:

.. code-block:: python

    class ArticlePage(MetadataPageMixin, Page):
        _metadata = {
            **MetadataPageMixin._metadata,
            # use the actual publish date, instead of the latest (possibly
            # unpublished) revision's timestamp
            "modified_time": "last_published_at",
        }

Both approaches can be freely combined, and work the same way for ``_schema`` and for adding custom tags/properties.

Schema.org support
------------------

``wagtail-metadata-mixin`` provides full support for `schema.org <https://schema.org/>`_ in
JSON-LD format, out of the box, through the ``_schema`` attribute.

In the same way as the basic ``_metadata`` attribute, ``_schema`` resolves and builds the
per-page Schema.org representation. As per ``_metadata``, its values can be the name of a
method, property or attribute available on the class. ``MetadataPageMixin`` already ships
with a sensible default:

.. code-block:: python

    _schema = {
        "name": "get_meta_title",
        "headline": "get_meta_title",
        "description": "get_meta_description",
        "image": "get_meta_image",
        "url": "get_meta_url",
        "author": "get_author_name",
        "datePublished": "published_time",
        "dateModified": "latest_revision_created_at",
    }

You can create your own schema, extending or overriding the default one, without having
to touch ``MetadataPageMixin`` itself:

.. code-block:: python

    class ArticlePage(MetadataPageMixin, Page):
        schemaorg_type = "Article"

        _schema = {
            **MetadataPageMixin._schema,
            "articleSection": "get_categories",
            "keywords": "get_keywords",
        }

        def get_categories(self):
            return list(self.categories.values_list("name", flat=True))

        def get_keywords(self):
            return self.get_meta_keywords()

Check django-meta_'s `schema.org documentation
<https://django-meta.readthedocs.io/en/latest/schema.html>`_ for more details.

Adding custom tags / properties
-------------------------------

Custom tags/properties can be added to your page without having to override the
``meta/meta.html`` template, by adding them to the ``_metadata`` attribute, as per the
other properties.

You can provide either a static value (see ``extra_props`` below), or the name of a
method which will return the value at runtime (see ``extra_custom_props``):

.. code-block:: python

    class CustomPage(MetadataPageMixin, Page):
        _metadata = {
            **MetadataPageMixin._metadata,
            "extra_props": {
                "designer": "Pablo Picasso",
            },
            "extra_custom_props": "get_custom_props",
        }

        def get_custom_props(self):
            return [
                ("property", "og:type", "music.song"),
                ("property", "music:duration", "3"),
            ]

``extra_props`` renders a ``<meta>`` tag per key/value pair, using the key as the
``name`` attribute:

.. code-block:: html

    <meta name="designer" content="Pablo Picasso">

``extra_custom_props`` takes a list of ``(attribute, name, value)`` tuples, letting you
pick the attribute used (e.g. ``property`` for Open Graph tags):

.. code-block:: html

    <meta property="og:type" content="music.song">
    <meta property="music:duration" content="3">

Check django-meta_'s `extra tags documentation
<https://django-meta.readthedocs.io/en/latest/extra_tags.html>`_ for more details.

Customising the search image rendition
--------------------------------------

By default, the search image rendition is set to ``fill-800x450``.

If you wish to use a different rendition, you can set the ``WAGTAILMETADATA_SEARCH_IMAGE_RENDITION``
setting to change the filter used. e.g.

.. code-block:: python

    WAGTAILMETADATA_SEARCH_IMAGE_RENDITION = "fill-1200x630"

Contributing
------------

If you like this module, forked it, or would like to improve it, please let us know!
Pull requests are welcome too. :-)

.. _django-meta: https://github.com/nephila/django-meta/

License
-------

``wagtail-metadata-mixin`` is released under the MIT license.
