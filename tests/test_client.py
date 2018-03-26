import base64
import hashlib
import hmac
import time

import pytest
from django.test import TestCase
from pretend import stub

from rest_framework_hmac.client import BaseHMACClient, HMACClient

from . import factory

ISO8601 = '%Y-%m-%dT%H:%M:%SZ'

TIME = time.strftime(ISO8601, time.gmtime())


class BaseHMACClientTests(TestCase):

    def test_get_user_secret(self):
        user = stub()

        with pytest.raises(NotImplementedError) as excinfo:
            BaseHMACClient(user)
        assert 'get_user_secret' in str(excinfo.value)


class HMACClientTests(TestCase):

    def _get_b64_signature(self, hmac_client, request, secret):
        string_to_sign = hmac_client.string_to_sign(request)
        byte_key = bytes.fromhex(secret)
        lhmac = hmac.new(byte_key, digestmod=hashlib.sha256)
        lhmac.update(string_to_sign.encode('utf8'))
        return base64.b64encode(lhmac.digest())

    def test_calc_signature(self):
        # covers the case of a POST / PUT request
        secret = '387632cfa3d18cd19bdfe72b61ac395dfcdc87c9'
        hmac_key = stub(secret=secret)
        user = stub(hmac_key=hmac_key)
        hmac_client = HMACClient(user)
        data = {'foo': 'bar'}
        request = factory.post_request(data)

        ret_b64 = hmac_client.calc_signature(request)

        b64 = self._get_b64_signature(hmac_client, request, secret)

        # uses the == comparison because not worried about a timing
        # attach in this test, so no need to use `hmac.compare_digest`
        # and also that function doesn't give a clear test failure
        assert ret_b64 == b64

    def test_calc_signature__request_has_no_data(self):
        # covers the case of a GET / DELETE request
        secret = '387632cfa3d18cd19bdfe72b61ac395dfcdc87c9'
        hmac_key = stub(secret=secret)
        user = stub(hmac_key=hmac_key)
        hmac_client = HMACClient(user)
        request = factory.get_request()

        ret_b64 = hmac_client.calc_signature(request)

        b64 = self._get_b64_signature(hmac_client, request, secret)

        assert ret_b64 == b64

    def test_calc_signature__fail(self):
        secret = '387632cfa3d18cd19bdfe72b61ac395dfcdc87c9'
        hmac_key = stub(secret=secret)
        user = stub(hmac_key=hmac_key)
        hmac_client = HMACClient(user)
        data = {'foo': 'bar'}
        request = factory.post_request(data)

        ret_b64 = hmac_client.calc_signature(request)

        b64 = self._get_b64_signature(hmac_client, request, secret='abc123')

        assert ret_b64 != b64
