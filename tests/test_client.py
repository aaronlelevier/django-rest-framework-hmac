import base64
import hashlib
import hmac
from collections import OrderedDict

from django.test import TestCase
from pretend import stub

from rest_framework_hmac.client import BaseHMAC, HMACAuthenticator, HMACSigner
from tests import factory


class BaseHMACTests(TestCase):

    def test_get_user_secret(self):
        secret = '387632cfa3d18cd19bdfe72b61ac395dfcdc87c9'
        hmac_key = stub(secret=secret)
        user = stub(hmac_key=hmac_key)

        base_hmac = BaseHMAC(user)

        assert base_hmac.secret == base_hmac.get_user_secret(user)


class HMACAuthenticatorTests(TestCase):

    def _get_b64_signature(self, authenticator, request, secret):
        string_to_sign = authenticator.string_to_sign(request)
        byte_key = bytes.fromhex(secret)
        lhmac = hmac.new(byte_key, digestmod=hashlib.sha256)
        lhmac.update(string_to_sign.encode('utf8'))
        return base64.b64encode(lhmac.digest())

    def test_calc_signature(self):
        # covers the case of a POST / PUT request
        secret = '387632cfa3d18cd19bdfe72b61ac395dfcdc87c9'
        hmac_key = stub(secret=secret)
        user = stub(hmac_key=hmac_key)
        authenticator = HMACAuthenticator(user)
        data = {'foo': 'bar'}
        request = factory.post_request(data)

        ret_b64 = authenticator.calc_signature(request)

        b64 = self._get_b64_signature(authenticator, request, secret)

        # uses the == comparison because not worried about a timing
        # attach in this test, so no need to use `hmac.compare_digest`
        # and also that function doesn't give a clear test failure
        assert ret_b64 == b64

    def test_calc_signature__request_has_no_data(self):
        # covers the case of a GET / DELETE request
        secret = '387632cfa3d18cd19bdfe72b61ac395dfcdc87c9'
        hmac_key = stub(secret=secret)
        user = stub(hmac_key=hmac_key)
        authenticator = HMACAuthenticator(user)
        request = factory.get_request()

        ret_b64 = authenticator.calc_signature(request)

        b64 = self._get_b64_signature(authenticator, request, secret)

        assert ret_b64 == b64

    def test_calc_signature__fail(self):
        secret = '387632cfa3d18cd19bdfe72b61ac395dfcdc87c9'
        hmac_key = stub(secret=secret)
        user = stub(hmac_key=hmac_key)
        authenticator = HMACAuthenticator(user)
        data = {'foo': 'bar'}
        request = factory.post_request(data)

        ret_b64 = authenticator.calc_signature(request)

        b64 = self._get_b64_signature(authenticator, request, secret='abc123')

        assert ret_b64 != b64


class HMACSignerTests(TestCase):

    def test_calc_signature(self):
        secret = '387632cfa3d18cd19bdfe72b61ac395dfcdc87c9'
        hmac_key = stub(secret=secret)
        user = stub(hmac_key=hmac_key)
        authenticator = HMACAuthenticator(user)
        data = {'foo': 'bar'}
        request = factory.post_request(data)
        authenticator_b64 = authenticator.calc_signature(request)

        headers = OrderedDict([
            ('method', 'POST'),
            ('hostname', '127.0.0.1'),
            ('path', '/'),
            ('timestamp', factory.TIME)
        ])
        signer_b64 = HMACSigner(user).calc_signature(headers, data)

        assert signer_b64 == authenticator_b64
