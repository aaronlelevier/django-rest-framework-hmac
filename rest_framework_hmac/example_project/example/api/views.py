from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_hmac.authentication import HMACAuthentication


class BlogView(APIView):

    authentication_classes = (HMACAuthentication,)

    def get(self, request, *args, **kwargs):
        return Response(data={'foo': 42})
