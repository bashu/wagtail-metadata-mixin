wagtail-metadata-mixin
======================

OpenGraph, Twitter Card and Google+ snippet tags for Wagtail CMS pages

Authored by `Basil Shubin <https://github.com/bashu>`_,  and some great
`contributors <https://github.com/bashu/wagtail-metadata-mixin/contributors>`_.

.. image:: https://img.shields.io/pypi/v/wagtail-metadata-mixin.svg
    :target: https://pypi.python.org/pypi/wagtail-metadata-mixin/

.. image:: https://img.shields.io/pypi/dm/wagtail-metadata-mixin.svg
    :target: https://pypi.python.org/pypi/wagtail-metadata-mixin/

.. image:: https://img.shields.io/github/license/bashu/wagtail-metadata-mixin.svg
    :target: https://pypi.python.org/pypi/wagtail-metadata-mixin/

.. image:: https://img.shields.io/travis/bashu/wagtail-metadata-mixin.svg
    :target: https://travis-ci.org/bashu/wagtail-metadata-mixin/

Requirements
------------

You must have *django-meta* installed and configured, see the
django-meta_ documentation for details and setup instructions.

The current version is tested for compatiblily with the following:

- Wagtail versions 2.0 to 2.8
- Django versions 1.11 to 3.0
- Python versions 3.4 to 3.8

Installation
============

First install the module, preferably in a virtual environment. It can be installed from PyPI:

.. code-block:: shell

    pip install wagtail-metadata-mixin

Setup
=====

Make sure the project is configured for django-meta_.

Then add the following settings:

.. code-block:: python

    INSTALLED_APPS += (
        'wagtailmetadata',
    )

and just include ``meta/meta.html`` template in your templates

.. code-block:: html+django

    {% load meta %}

    <html>
        <head {% meta_namespaces %}>
            {% include "meta/meta.html" %}
        </head>
        <body>...</body>
    </html>

Usage
=====

.. code-block:: python

    # models.py

    from wagtail.core.models import Page, PageBase

    from wagtailmetadata.models import MetadataPageMixin

    # ensure MetadataPageMixin class goes before Page class
    class CustomPage(MetadataPageMixin, Page):
        promote_panels = Page.promote_panels + MetadataPageMixin.panels

Contributing
------------

If you like this module, forked it, or would like to improve it, please let us know!
Pull requests are welcome too. :-)

.. _django-meta: https://github.com/nephila/django-meta/
