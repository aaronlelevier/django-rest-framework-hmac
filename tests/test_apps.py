from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

from rest_framework_hmac.apps import HMACConfig


class HMACConfigTests(TestCase):

    def test_config(self):
        assert HMACConfig.name == 'rest_framework_hmac'
        assert HMACConfig.verbose_name == _("Django REST Framework HMAC")
