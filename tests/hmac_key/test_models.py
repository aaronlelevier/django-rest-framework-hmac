import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.test import TestCase

from rest_framework_hmac.hmac_key.models import HMACKey


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_hmac_key(sender, instance=None, created=False, **kwargs):
    if created:
        HMACKey.objects.create(user=instance)


class HMACKeyTests(TestCase):

    def test_create_hmac_key(self):
        user = User.objects.create_user('bob')

        assert isinstance(user.hmac_key, HMACKey)
        hmac_key = user.hmac_key
        # key
        assert isinstance(hmac_key.key, str)
        assert len(hmac_key.key) == 40
        # secret
        assert isinstance(hmac_key.secret, str)
        assert len(hmac_key.secret) == 40
        # user
        assert hmac_key.user == user
        # created
        assert isinstance(hmac_key.created, datetime.datetime)
        # __str__
        assert hmac_key.key == str(hmac_key)
