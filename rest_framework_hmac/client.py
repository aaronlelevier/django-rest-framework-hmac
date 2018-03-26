import base64
import hashlib
import hmac
import json


class BaseHMACClient(object):
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

    def calc_signature(self, request):
        """
        Calculates the HMAC signature based upon the cryptographic key
        and the request payload
        """
        string_to_sign = self.string_to_sign(request)
        byte_key = bytes.fromhex(self.secret)
        lhmac = hmac.new(byte_key, digestmod=hashlib.sha256)
        lhmac.update(string_to_sign.encode('utf8'))
        return base64.b64encode(lhmac.digest())

    def string_to_sign(self, request):
        """
        Uses the request.path, method, timestamp of the request,
        and optionally the payload, if it's not a GET, to determine
        the string used for signing
        """
        s = '%s\n%s\n%s\n%s\n' % (request.method,
                                  request.META['REMOTE_ADDR'],
                                  request.META['PATH_INFO'],
                                  request.META['Timestamp'])

        # Don't add in case of a 'GET' request
        if getattr(request, 'data', None):
            s += json.dumps(request.data, separators=(',', ':'))

        return s

    def get_user_secret(self, user):
        raise NotImplementedError('get_user_secret')


class HMACClient(BaseHMACClient):
    """
    Concrete class for HMAC Client cryptographic signing. Use
    this class if the programmer has registered the HMACKey
    Model to be created via a signal
    """
    def get_user_secret(self, user):
        return user.hmac_key.secret
