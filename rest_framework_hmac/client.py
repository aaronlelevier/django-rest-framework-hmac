import base64
import hashlib
import hmac
import json
from collections import OrderedDict


class BaseHMAC(object):
    """
    Base class for HMAC Client cryptographic signing. Use
    this class if the programmer wants to implement thier
    own lookup for the HMAC `secret` cryptographic key
    """
    def __init__(self, user):
        """
        Args:
            user (User instance):
                that will be used to obtain the cryptographic key
        """
        self.secret = self.get_user_secret(user)

    def get_user_secret(self, user):
        return user.hmac_key.secret

    def _calc_signature_from_str(self, s):
        byte_key = bytes.fromhex(self.secret)
        lhmac = hmac.new(byte_key, digestmod=hashlib.sha256)
        lhmac.update(s.encode('utf8'))
        return base64.b64encode(lhmac.digest())


class HMACAuthenticator(BaseHMAC):
    """
    Concrete class for HMACAuthenticator cryptographic signing.
    Use this class if the programmer has registered the HMACKey
    Model to be created via a signal
    """
    def calc_signature(self, request):
        """
        Calculates the HMAC signature based upon the cryptographic key
        and the request payload
        """
        string_to_sign = self.string_to_sign(request)
        return self._calc_signature_from_str(string_to_sign)

    def string_to_sign(self, request):
        """
        Uses the request.path, method, timestamp of the request,
        and optionally the payload, if it's not a GET, to determine
        the string used for signing
        """
        headers = OrderedDict([
            ('method', request.method),
            ('hostname', request.META['REMOTE_ADDR']),
            ('path', request.META['PATH_INFO']),
            ('timestamp', request.META['Timestamp'])
        ])
        s = '{method}\n{hostname}\n{path}\n{timestamp}\n'.format(**headers)

        # Don't add in case of a 'GET' request
        if getattr(request, 'data', None):
            s += json.dumps(request.data, separators=(',', ':'))

        return s


class HMACSigner(BaseHMAC):
    """
    Conveince class for signing HMAC request Signatures using
    and OrderedDict instead of a request, which is what the
    `HMACAuthenticator` relies on for calculating the HMAC
    Signatures
    """
    def calc_signature(self, headers, data):
        string_to_sign = self.string_to_sign(headers, data)
        return self._calc_signature_from_str(string_to_sign)

    def string_to_sign(self, headers, data):
        s = '{method}\n{hostname}\n{path}\n{timestamp}\n'.format(**headers)

        # Don't add in case of a 'GET' request
        if data:
            s += json.dumps(data, separators=(',', ':'))

        return s
