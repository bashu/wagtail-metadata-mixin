DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.contenttypes',

    'taggit',
    'modelcluster',

    'wagtail.wagtailcore',
    'wagtail.wagtailusers',
    'wagtail.wagtailimages',

    'meta',
    'wagtailmetadata',
]

ROOT_URLCONF = 'test_urls'
