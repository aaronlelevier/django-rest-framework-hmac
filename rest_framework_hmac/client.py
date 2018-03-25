import base64
import hashlib
import hmac
import json


class HMACClient(object):

    def __init__(self, secret_key):
        """
        Args:
            secret_key (byte str): cryptographic key
        """
        self.secret_key = secret_key

    def calc_signature(self, request):
        """
        Calculates the HMAC signature based upon the cryptographic key
        and the request payload
        """
        string_to_sign = json.dumps(request.data, separators=(',', ':'))
        byte_key = bytes.fromhex(self.secret_key)
        lhmac = hmac.new(byte_key, digestmod=hashlib.sha256)
        lhmac.update(string_to_sign.encode('utf8'))
        return base64.b64encode(lhmac.digest())
