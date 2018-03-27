import pytest
from django.contrib.auth.models import User
from django.test import TestCase
from pretend import stub
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.views import APIView

from rest_framework_hmac.authentication import HMACAuthentication
from rest_framework_hmac.client import HMACSigner
from tests import factory

request_factory = APIRequestFactory()

ISO8601 = '%Y-%m-%dT%H:%M:%SZ'


class BasicView(APIView):
    authentication_classes = (HMACAuthentication,)

    def get(self, request, *args, **kwargs):
        return Response(data={'foo': 'bar'})

    def post(self, request, *args, **kwargs):
        return Response(data=request.data)

    def put(self, request, *args, **kwargs):
        return Response(data=request.data)

    def delete(self, request, *args, **kwargs):
        return Response(data={'message': 'ok'})


class HMACAuthenticationUnitTests(TestCase):

    def test_get_user(self):
        user = User.objects.create_user('bob')
        request = stub(META={'Key': user.hmac_key.key})

        ret = HMACAuthentication().get_user(request)

        assert ret == user

    def test_get_user__fail_if_key_not_sent(self):
        request = stub(META={})

        with pytest.raises(AuthenticationFailed):
            HMACAuthentication().get_user(request)

    def test_get_user__fail_if_invalid_key(self):
        request = stub(META={'Key': 'invalid'})

        with pytest.raises(AuthenticationFailed):
            HMACAuthentication().get_user(request)

    def test_get_signature(self):
        signature = b'my-signature'
        request = stub(META={'Signature': signature})

        ret = HMACAuthentication().get_signature(request)

        assert ret == signature

    def test_get_signature__fail_if_key_not_sent(self):
        request = stub(META={})

        with pytest.raises(AuthenticationFailed):
            HMACAuthentication().get_signature(request)

    def test_get_signature__fail_if_not_bytes(self):
        signature = 'str'
        request = stub(META={'Signature': signature})

        with pytest.raises(AuthenticationFailed):
            HMACAuthentication().get_signature(request)


class HMACAuthenticationIntegrationTests(APITestCase):

    def setUp(self):
        self.post_data = {'foo': 'bar'}
        self.user = User.objects.create_user('bob')
        self.view = BasicView.as_view()
        self.extras = {'Key': self.user.hmac_key.key, 'Timestamp': factory.TIME}

    def test_post_200(self):
        self.extras['Signature'] = HMACSigner(self.user).calc_signature(
            factory.post_headers, self.post_data)

        request = request_factory.post(
            '/', self.post_data, format='json', **self.extras)
        response = self.view(request)

        assert response.status_code == status.HTTP_200_OK

    def test_post_400__invalid_signature(self):
        self.extras['Signature'] = b'invalid'

        request = request_factory.post(
            '/', self.post_data, format='json', **self.extras)
        response = self.view(request)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_200(self):
        self.extras['Signature'] = HMACSigner(self.user).calc_signature(
            factory.get_headers)

        request = request_factory.get('/', format='json', **self.extras)
        response = self.view(request)

        assert response.status_code == status.HTTP_200_OK

    def test_put_200(self):
        data = {'biz': 'baz'}
        self.extras['Signature'] = HMACSigner(self.user).calc_signature(
            factory.put_headers, data)

        request = request_factory.put('/', data, format='json', **self.extras)
        response = self.view(request)

        assert response.status_code == status.HTTP_200_OK

    def test_delete_200(self):
        self.extras['Signature'] = HMACSigner(self.user).calc_signature(
            factory.delete_headers)

        request = request_factory.delete('/', format='json', **self.extras)
        response = self.view(request)

        assert response.status_code == status.HTTP_200_OK
