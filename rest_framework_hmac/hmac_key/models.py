import binascii
import os

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class HMACKey(models.Model):
    """
    The default HMACKey model that can auto generate a
    key/secret for HMAC Auth via a signal
    """
    def generate_key():
        """
        Returns a 40 character hex string based on binary random data
        """
        return binascii.hexlify(os.urandom(20)).decode()

    key = models.CharField(
        _("Key"), primary_key=True, max_length=40, default=generate_key)
    secret = models.CharField(
        _("Secret"), max_length=40, default=generate_key)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='hmac_key',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        # Only create a DB table for this Model if this app is registered
        abstract = 'rest_framework_hmac.hmac_key' \
            not in settings.INSTALLED_APPS
        verbose_name = _("HMACKey")
        verbose_name_plural = _("HMACKey")

    def __str__(self):
        return self.key
