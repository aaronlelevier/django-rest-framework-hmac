import base64
import hashlib
import hmac
import json

import pytest
from django.test import TestCase
from pretend import stub

from rest_framework_hmac.client import BaseHMACClient, HMACClient


class BaseHMACClientTests(TestCase):

    def test_get_user_secret(self):
        user = stub()

        with pytest.raises(NotImplementedError) as excinfo:
            BaseHMACClient(user)
        assert 'get_user_secret' in str(excinfo.value)


class HMACClientTests(TestCase):

    def test_calc_signature(self):
        secret = '387632cfa3d18cd19bdfe72b61ac395dfcdc87c9'
        hmac_key = stub(secret=secret)
        user = stub(hmac_key=hmac_key)
        hmac_client = HMACClient(user)
        data = {'foo': 'bar'}
        request = stub(data=data)

        ret_b64 = hmac_client.calc_signature(request)

        string_to_sign = json.dumps(request.data, separators=(',', ':'))
        byte_key = bytes.fromhex(secret)
        lhmac = hmac.new(byte_key, digestmod=hashlib.sha256)
        lhmac.update(string_to_sign.encode('utf8'))
        b64 = base64.b64encode(lhmac.digest())

        # uses the == comparison because not worried about a timing
        # attach in this test, so no need to use `hmac.compare_digest`
        # and also that function doesn't give a clear test failure
        assert ret_b64 == b64
