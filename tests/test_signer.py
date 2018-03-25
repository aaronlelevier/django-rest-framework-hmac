import base64
import hashlib
import hmac

from django.test import TestCase
from pretend import stub

from rest_framework_hmac import HMACSigner


class SignerTests(TestCase):

    def setUp(self):
        self.api_key = '387632cfa3d18cd19bdfe72b61ac395dfcdc87c9'

    def test_calc_signature(self):
        hmac_signer = HMACSigner(self.api_key)
        data = {'foo': 'bar'}
        request = stub(data=data)

        ret_b64, params = hmac_signer.calc_signature(request)

        ret_qs = hmac_signer.string_to_sign(params)
        byte_key = bytes.fromhex(self.api_key)
        lhmac = hmac.new(byte_key, digestmod=hashlib.sha256)
        lhmac.update(ret_qs.encode('utf8'))
        b64 = base64.b64encode(lhmac.digest())

        assert hmac.compare_digest(ret_b64, b64)

    def test_add_request_header(self):
        hmac_signer = HMACSigner(self.api_key)
        data = {'foo': 'bar'}
        request = stub(data=data)

        b64, params = hmac_signer.calc_signature(request)
        
        ret = HMACSigner(self.api_key).add_request_header(request)

        assert ret == request
        assert ret.META.get('Signature') == b64

        for k, v in params.items():
            assert ret.META[k] == v
