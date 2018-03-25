import base64
import hashlib
import hmac
import json
import time
from urllib.parse import quote

import six

ISO8601 = '%Y-%m-%dT%H:%M:%SZ'


class HMACClient(object):

    def __init__(self, secret_key):
        self.secret_key = secret_key

    def calc_signature(self, request):
        string_to_sign = json.dumps(request.data, separators=(',', ':'))
        byte_key = bytes.fromhex(self.secret_key)
        lhmac = hmac.new(byte_key, digestmod=hashlib.sha256)
        lhmac.update(string_to_sign.encode('utf8'))
        b64 = base64.b64encode(lhmac.digest())
        return b64
