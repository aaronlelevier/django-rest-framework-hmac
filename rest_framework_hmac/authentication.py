import hmac

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from rest_framework_hmac.client import HMACClient


class HMACAuthentication(BaseAuthentication):

    def authenticate(self, request):
        signature = self.get_signature(request)
        user = self.get_user(request)

        b64 = HMACClient(user.hmac_key.secret).calc_signature(request)

        if not hmac.compare_digest(b64, signature):
            raise AuthenticationFailed()

        return (user, None)

    def get_user(self, request):
        # TODO: getting AppsNotConfigured error, so put this import here,
        # there should be a config to not get that error
        from django.contrib.auth import get_user_model
        UserModel = get_user_model()

        try:
            return UserModel.objects.get(hmac_key__key=request.META['Key'])
        except (KeyError, UserModel.DoesNotExist):
            raise AuthenticationFailed()

    def get_signature(self, request):
        try:
            signature = request.META['Signature']
        except KeyError:
            raise AuthenticationFailed()

        if not isinstance(signature, bytes):
            raise AuthenticationFailed()

        return signature
