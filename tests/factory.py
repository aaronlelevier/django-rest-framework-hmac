import time

from pretend import stub

ISO8601 = '%Y-%m-%dT%H:%M:%SZ'

TIME = time.strftime(ISO8601, time.gmtime())


def post_request(data):
    return _request_with_data(data, method='POST')


def put_request(data):
    return _request_with_data(data, method='PUT')


def _request_with_data(data, method):
    return stub(
        method=method,
        META={
            'REMOTE_ADDR': '127.0.0.1',
            'PATH_INFO': '/',
            'Timestamp': TIME
        },
        data=data)


def get_request():
    return _request_without_data(method='GET')


def delete_request():
    return _request_without_data(method='DELETE')


def _request_without_data(method):
    return stub(
        method=method,
        META={
            'REMOTE_ADDR': '127.0.0.1',
            'PATH_INFO': '/',
            'Timestamp': TIME
        })
