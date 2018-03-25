import base64
import hashlib
import hmac
import json
import time
from urllib.parse import quote

import six

ISO8601 = '%Y-%m-%dT%H:%M:%SZ'


class HMACSigner(object):

    def __init__(self, api_key):
        self.api_key = api_key

    def calc_signature(self, request):
        params = {
            'SignatureVersion': '1',
            'SignatureMethod': 'HmacSHA256',
            'Timestamp': time.strftime(ISO8601, time.gmtime()),
            'SecurityToken': self.api_key,
            'Content': json.dumps(request.data, separators=(',', ':'))
        }

        string_to_sign = self.string_to_sign(params)

        byte_key = bytes.fromhex(self.api_key)
        lhmac = hmac.new(byte_key, digestmod=hashlib.sha256)
        lhmac.update(string_to_sign.encode('utf8'))
        b64 = base64.b64encode(lhmac.digest())

        return b64, params

    def string_to_sign(self, params):
        pairs = []
        for key in sorted(params):
            # So an idempotent signature is generated. This will skip
            # the Signature key if already set, in the case of a retry.
            if key == 'Signature':
                continue
            value = six.text_type(params[key])
            pairs.append(quote(key.encode('utf-8'), safe='') + '=' +
                         quote(value.encode('utf-8'), safe='-_~'))
        return '&'.join(pairs)

    def add_request_header(self, request):
        b64, params = self.calc_signature(request)
        if not getattr(request, 'META', None):
            request.META = {}

        request.META.update(params)
        request.META['Signature'] = b64

        return request
