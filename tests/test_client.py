import base64
import hashlib
import hmac
import json

from django.test import TestCase
from pretend import stub

from rest_framework_hmac import HMACClient


class SignerTests(TestCase):

    def setUp(self):
        self.api_key = '387632cfa3d18cd19bdfe72b61ac395dfcdc87c9'

    def test_calc_signature(self):
        hmac_client = HMACClient(self.api_key)
        data = {'foo': 'bar'}
        request = stub(data=data)

        ret_b64 = hmac_client.calc_signature(request)

        string_to_sign = json.dumps(request.data, separators=(',', ':'))
        byte_key = bytes.fromhex(self.api_key)
        lhmac = hmac.new(byte_key, digestmod=hashlib.sha256)
        lhmac.update(string_to_sign.encode('utf8'))
        b64 = base64.b64encode(lhmac.digest())

        # uses the == comparison because not worried about a timing
        # attach in this test, so no need to use `hmac.compare_digest`
        # and also that function doesn't give a clear test failure
        assert ret_b64 == b64
