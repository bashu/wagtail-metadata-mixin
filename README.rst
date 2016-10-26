wagtail-metadata-mixin
======================

OpenGraph, Twitter Card and Google+ snippet tags for Wagtail CMS pages

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

    <html {% meta_namespaces_gplus %}>
        <head {% meta_namespaces %}>
            {% include "meta/meta.html" %}
        </head>
        <body>...</body>
    </html>

Usage
=====

.. code-block:: python

    # models.py

    from django.utils import six
    from wagtail.wagtailcore.models import Page, PageBase

    from wagtailmetadata.models import MetadataPageMixin


    class CustomPage(six.with_metaclass(PageBase, MetadataPageMixin, Page)):
        promote_panels = Page.promote_panels + MetadataPageMixin.panels


Please see ``example`` application. This application is used to manually test the functionalities of this package. This also serves as good example...

You need Django 1.8.1 or above to run that. It might run on older versions but that is not tested.

Contributing
------------

If you like this module, forked it, or would like to improve it, please let us know!
Pull requests are welcome too. :-)

.. _django-meta: https://github.com/nephila/django-meta/
