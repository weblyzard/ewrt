#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from urllib.error import HTTPError

from eWRT.ws.rest import MultiRESTClient, RESTClient

    
class TestRESTClient(unittest.TestCase):

    TEST_URL = 'http://httpbin.org/basic-auth/user/passwd'
    TEST_USER = 'user'
    TEST_PASS = 'passwd'

    def test_retrieve(self):
        r = RESTClient(self.TEST_URL, self.TEST_USER, self.TEST_PASS)
        try:
            r._json_request(self.TEST_URL)
        except HTTPError as e:
            # authentification succeeded, but no object could
            # be found
            assert '404: Not Found' in str(e)

    def test_multi_request(self):
        urls = (('http://irgendwas.com', None, None),
                ('http://heinz:secret@irgendwas.com', 'heinz', 'secret'))
        service_urls = [url[0] for url in urls]
        client = MultiRESTClient(service_urls)

        for i, (service_url, user, passwd) in enumerate(urls):
            c = client.clients[i]
            if user:
                assert service_url != c.service_url
            assert c.user == user
            assert c.password == passwd

        try:
            client.request('irgendwas')
            assert False
        except Exception as e:
            assert 'Could not make request to path' in str(e)

        try:
            urls = ('https://heinz@irgendwas.com', )
            client = MultiRESTClient(urls)
            assert False, 'must raise an assertion error'
        except Exception as e:
            print('!!! previous exception is OK, we expected that')
            assert 'if set, user AND pwd required' in e.args # not tested (SV)

    def test_get_url(self):
        assert RESTClient.get_request_url(self.TEST_URL, 'execute', '12') \
            .endswith("/execute/12")
        assert RESTClient.get_request_url(
            self.TEST_URL,
            'execute',
            '12',
            {'debug': True}).endswith("/execute/12?debug=True")

    def test_fix_url(self):
        ''' tests fix url '''

    def test_randomize_urls(self):
        ''' this test might fail, if random returns the same list, but this is
        very unlikely '''
        client = MultiRESTClient(service_urls='http://test.url',
                                 use_random_server=True)

        assert isinstance(client._service_urls, list)
        assert len(client._service_urls) == 1

        service_urls = ['http://test.url%s' % i for i in range(1000)]

        client = MultiRESTClient(service_urls=service_urls,
                                 use_random_server=True)

        assert len(client._service_urls) == len(service_urls)
        assert service_urls != client._service_urls

if __name__ == '__main__':
    unittest.main()