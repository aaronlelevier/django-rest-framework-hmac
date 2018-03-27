import time

from pretend import stub

ISO8601 = '%Y-%m-%dT%H:%M:%SZ'

TIME = time.strftime(ISO8601, time.gmtime())


def post_request(data):
    return stub(
        method='POST',
        META={
            'REMOTE_ADDR': '127.0.0.1',
            'PATH_INFO': '/',
            'Timestamp': TIME
        },
        data=data)


def get_request():
    return stub(
        method='GET',
        META={
            'REMOTE_ADDR': '127.0.0.1',
            'PATH_INFO': '/',
            'Timestamp': TIME
        })


def _headers(method):
    return {
        'method': method,
        'hostname': '127.0.0.1',
        'path': '/',
        'timestamp': TIME
    }


get_headers = _headers('GET')

post_headers = _headers('POST')

put_headers = _headers('PUT')

delete_headers = _headers('DELETE')
