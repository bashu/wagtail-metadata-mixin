Changes
-------

3.0.1 (2026-08-15)
~~~~~~~~~~~~~~~~~~

* Added og/twitter/schemaorg title and description fields, JSON-LD toggle, and OG
  type/app_id/profile_id/publisher/author_url fields, matching django-meta's current API.
* Added full support for schema.org in JSON-LD format via the ``_schema`` attribute.
* Fixed ``get_meta_image_width()``/``get_meta_image_height()`` to build off a rendition,
  consistent with ``get_meta_image()``.
* Fixed ``get_meta_site_name()``, ``get_domain()`` and ``build_absolute_uri()`` to no
  longer crash silently when used on a non-``Page`` model.

3.0.0 (2026-08-15)
~~~~~~~~~~~~~~~~~~

* Bumped requirements: Wagtail 6.3+, Django 5.2/6.0/6.1, Python 3.10+, django-meta 2.5+.

2.0.2 (2021-11-29)
~~~~~~~~~~~~~~~~~~

* Fixed stupid typo.

2.0.1 (2021-11-29)
~~~~~~~~~~~~~~~~~~

* Added ru translation.

2.0.0 (2021-11-28)
~~~~~~~~~~~~~~~~~~

* Added Wagtail 2.15 and Django 3.2 support.
* Dropped Wagtail 2.7 support.
