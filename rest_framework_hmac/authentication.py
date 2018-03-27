import hmac

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from rest_framework_hmac.client import HMACAuthenticator


class HMACAuthentication(BaseAuthentication):

    def authenticate(self, request):

        signature = self.get_signature(request)
        user = self.get_user(request)

        b64 = HMACAuthenticator(user).calc_signature(request)

        if not hmac.compare_digest(b64, signature):
            raise AuthenticationFailed()

        return (user, None)

    @staticmethod
    def get_user(request):
        from django.contrib.auth import get_user_model
        UserModel = get_user_model()

        try:
            return UserModel.objects.get(hmac_key__key=request.META['Key'])
        except (KeyError, UserModel.DoesNotExist):
            raise AuthenticationFailed()

    @staticmethod
    def get_signature(request):
        try:
            signature = request.META['Signature']
        except KeyError:
            raise AuthenticationFailed()

        if not isinstance(signature, bytes):
            raise AuthenticationFailed()

        return signature
