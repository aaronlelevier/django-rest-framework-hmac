from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

from rest_framework_hmac.hmac_key.apps import HMACKeyConfig


class HMACKeyConfigTests(TestCase):

    def test_config(self):
        assert HMACKeyConfig.name == 'rest_framework_hmac.hmac_key'
        assert HMACKeyConfig.verbose_name == _("HMAC Key")
