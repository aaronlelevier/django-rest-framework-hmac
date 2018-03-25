import binascii
import os

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
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

    def __str__(self):
        return self.key
