import sys
from os.path import dirname, join

import pytest


def exit_on_failure(ret, message=None):
    if ret:
        sys.exit(ret)


def configure_settings():
    from django.conf import settings

    # If DJANGO_SETTINGS_MODULE envvar exists the settings will be
    # configured by it. Otherwise it will use the parameters bellow.
    if not settings.configured:
        params = dict(
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            INSTALLED_APPS=(
                'django.contrib.contenttypes',
                'django.contrib.auth',
                'rest_framework_hmac.hmac_key'
            ),
            SITE_ID=1,
            TEST_RUNNER='django.test.simple.DjangoTestSuiteRunner',
            TEST_ROOT=join(dirname(__file__), 'tests'),
            MIDDLEWARE_CLASSES=(),
        )
        # Configure Django's settings
        settings.configure(**params)
    
    return settings


if __name__ == "__main__":
    configure_settings()
    exit_on_failure(pytest.main(sys.argv))
