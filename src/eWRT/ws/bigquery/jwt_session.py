#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 25.02.2015

@author: Christian Junker
"""
import json
import unittest
import os
from datetime import datetime, timedelta

from oauth2client.client import SignedJwtAssertionCredentials
from httplib2 import ServerNotFoundError

from eWRT.config import BIG_QUERY_CERTIFICATE_FILENAME


def inject(fun):
    def jwt_injected(*args, **kwargs):
        if kwargs.get('session') is None:
            with JWTSession() as jwt_session:
                kwargs['session'] = jwt_session
                return fun(*args, **kwargs)
        else:
            return fun(*args, **kwargs)

    return jwt_injected


class JWTSession(object):
    def __init__(self, certificate_filename=BIG_QUERY_CERTIFICATE_FILENAME):
        if certificate_filename is None:
            raise ValueError("certificate filename must not be None")
        with open(certificate_filename) as jwt_file:
            self._jwt_json_data = json.load(jwt_file)

        self._credential = SignedJwtAssertionCredentials(
            self._jwt_json_data['client_email'],
            self._jwt_json_data['private_key'],
            'https://www.googleapis.com/auth/bigquery')
        self._access_token_info = None
        self._expires_at = 0

    def is_alive(self):
        return self._expires_at > datetime.now()

    def get_remaining_time(self):
        return self._expires_at - datetime.now()

    def get_header_item(self):
        return 'Authorization', 'Bearer ' + self.get_token()

    def get_token(self):
        if self._access_token_info is None:
            return None
        else:
            return self._access_token_info.access_token

    def __enter__(self):
        # using a context manager because tokens have to be regenerated
        self._access_token_info = self._credential.get_access_token()
        self._expires_at = datetime.now() + timedelta(seconds=self._access_token_info.expires_in)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._access_token_info = None


# TODO put into utility class
class NoInternet(object):
    def __init__(self, exception):
        self._exception = exception

    def __call__(self, fun):
        def decorated_fun(*args, **kwargs):
            # https://stackoverflow.com/questions/23351796/django-block-internet-connection-for-testing-purposes
            # Block Internet access during tests
            import urllib2
            import httplib
            import httplib2

            def _raise_http_error(*args, **kwargs):
                raise self._exception("I told you not to use the Internet!")

            class AngryHandler(urllib2.BaseHandler):
                handler_order = 1

                def default_open(self, _):
                    _raise_http_error()

            opener = urllib2.build_opener(AngryHandler)
            urllib2.install_opener(opener)

            _http_handler = urllib2.HTTPHandler
            _https_handler = urllib2.HTTPSHandler
            urllib2.HTTPHandler = AngryHandler
            urllib2.HTTPSHandler = AngryHandler

            _http_connect = httplib.HTTPConnection.connect
            _https_connect = httplib.HTTPSConnection.connect
            _http_request = httplib.HTTPConnection.request
            _https_request = httplib.HTTPSConnection.request
            _http2_request = httplib2.Http.request

            httplib.HTTPConnection.connect = lambda _: None
            httplib.HTTPSConnection.connect = lambda _: None
            httplib.HTTPConnection.request = _raise_http_error
            httplib.HTTPSConnection.request = _raise_http_error
            httplib2.Http.request = _raise_http_error

            try:
                return fun(*args, **kwargs)
            finally:
                base_opener = urllib2.build_opener(urllib2.BaseHandler)
                urllib2.install_opener(base_opener)
                urllib2.HTTPHandler = _http_handler
                urllib2.HTTPSHandler = _https_handler

                httplib.HTTPConnection.connect = _http_connect
                httplib.HTTPSConnection.connect = _https_connect
                httplib.HTTPConnection.request = _http_request
                httplib.HTTPSConnection.request = _https_request
                httplib2.Http.request = _http2_request

        return decorated_fun


class JWTSessionTest(unittest.TestCase):
    @staticmethod
    def _real_file_name(file_name):
        return os.path.sep.join((os.path.dirname(os.path.realpath(__file__)), file_name))

    def test_file_missing(self):
        self.assertRaises(ValueError, JWTSession, certificate_filename=None)
        self.assertRaises(IOError, JWTSession, certificate_filename='non_existent')

    def test_invalid_certificate(self):
        self.assertRaises(ValueError, JWTSession, certificate_filename=self._real_file_name('bq_invalid_json.json'))

        invalid_jwt_session = JWTSession(certificate_filename=self._real_file_name('bq_invalid_key.json'))
        self.assertRaises(Exception, invalid_jwt_session.__enter__)  # todo too unspecific
        self.assertIsNone(invalid_jwt_session._access_token_info)

    def test_normal_operation(self):
        @inject
        def injected(session=None):
            self.assertIsNotNone(session)
            self.assertIsNotNone(session.get_token())
            self.assertTrue(session.is_alive())

        injected

    def test_header_generation(self):
        @inject
        def injected(session=None):
            auth_key, auth_value = session.get_header_item()
            self.assertEquals(auth_key, 'Authorization')
            self.assertEquals(auth_value, 'Bearer ' + session.get_token())

        injected()

    @NoInternet(ServerNotFoundError)
    def test_no_internet(self):
        injected = inject(lambda session: None)
        self.assertRaises(ServerNotFoundError, injected)


if __name__ == '__main__':
    unittest.main()
