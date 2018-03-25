from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class HMACKeyConfig(AppConfig):
    name = 'rest_framework_hmac.hmac_key'
    verbose_name = _("HMAC Key")
