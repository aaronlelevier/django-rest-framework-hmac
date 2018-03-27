import time

from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from rest_framework_hmac.client import HMACSigner

ISO8601 = '%Y-%m-%dT%H:%M:%SZ'

TIME = time.strftime(ISO8601, time.gmtime())


class ViewTests(APITestCase):

    def test_get_403_not_authenticated(self):
        response = self.client.get('/api/blog/')

        self.assertEqual(response.status_code, 403, response.data)

    def test_get_200(self):
        user = User.objects.create_user('bob')
        headers = {
            'method': 'GET',
            'hostname': '127.0.0.1',
            'path': '/api/blog/',
            'timestamp': TIME
        }
        signature = HMACSigner(user).calc_signature(headers)

        response = self.client.get(
            '/api/blog/',
            **{'Key': user.hmac_key.key, 'Timestamp': TIME, 'Signature': signature})

        self.assertEqual(response.status_code, 200, response.data)
