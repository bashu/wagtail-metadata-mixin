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

- Wagtail versions 6.3 to 7.4
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

Contributing
------------

If you like this module, forked it, or would like to improve it, please let us know!
Pull requests are welcome too. :-)

.. _django-meta: https://github.com/nephila/django-meta/

License
-------

``wagtail-metadata-mixin`` is released under the MIT license.
