from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework_hmac.hmac_key.models import HMACKey


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_hmac_key(sender, instance=None, created=False, **kwargs):
    if created:
        HMACKey.objects.create(user=instance)
