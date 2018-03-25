from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class HMACConfig(AppConfig):
    name = 'rest_framework_hmac'
    verbose_name = _("Django REST Framework HMAC")
