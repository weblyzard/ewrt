#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
:package: eWRT.ws.wot

:author: Heinz-Peter Lang

Client for accessing the Reputation API for Web of Trust

see: `WOT API Documentation <http://www.mywot.com/wiki/API#Documentation:_Reputation_API>`_
'''
import unittest
import json
from urllib import urlencode, quote
from urlparse import urlparse

from eWRT.access.http import Retrieve

SERVICE_URL = 'http://api.mywot.com/0.4/public_link_json2?hosts=%(hosts)s&key=%(api_key)s'
WOT_LINK = 'http://www.mywot.com/en/scorecard/%s'
MAX_HOSTS = 100

MAPPING = {'0': 'trustworthiness',
           '1': 'vendor_reliability',
           '2': 'privacy',
           '4': 'child_safety',
           'target': 'target'}

class WebOfTrust(object):
    
    def __init__(self, api_key, service_url=SERVICE_URL):
        self.api_key = api_key
        self.service_url = service_url
        self.retrieve = Retrieve('eWRT.ws.wot')
        
    def get_reputation(self, hosts): 
        query={'hosts': self._encode_hosts(hosts),
               'api_key': self.api_key}
        
        urlObj = self.retrieve.open(self.service_url % query)
        
        if not urlObj:
            raise Exception('got no result')
        
        return self._format_result(json.loads(urlObj.read())) 
        
    @classmethod
    def _encode_hosts(cls, hosts):
        ''' 
        >>> WebOfTrust._encode_hosts(['http://wu.ac.at', 'https://wu.ac.at'])
        'wu.ac.at/'
        >>> WebOfTrust._encode_hosts(['wu.ac.at', 'https://modul.ac.at/'])
        'wu.ac.at/modul.ac.at/'
        '''
        if isinstance(hosts, basestring):
            hosts = [hosts]
        
        selected_hosts = []
        
        for host in hosts:
            
            if not host.startswith('http'):
                host = 'http://%s' % host
            netloc = '%s/' % quote(urlparse(host).netloc)
            
            if not netloc in selected_hosts: 
                selected_hosts.append(netloc)
        
        assert len(hosts) <= MAX_HOSTS, 'too many hosts (max: %s)!' % MAX_HOSTS
        return ''.join(selected_hosts)
    
    @classmethod
    def _encode_url(cls, service_url, query):
        ''' encodes the url '''
        return service_url % query

    @classmethod
    def _format_result(cls, data):
        '''
        Formats the result using MAPPING. The components for the reputation 
        provide the reputation and confidence. See WOT Developer API for 
        details
        '''
        result = {}
        for host, reputation in data.iteritems():
            r = {}
            for attr_name, new_attr_name in MAPPING.iteritems():
                if attr_name in reputation:
                    r[new_attr_name] = reputation[attr_name]
            r['wot_link'] = WOT_LINK % r['target']
            result[host] = r
            
        return result

class TestWOT(unittest.TestCase):
    
    def test_format_result(self):
        data = {u'diepresse.com': {u'1': [93, 54], u'0': [92, 57], 
                                   u'2': [93, 54], u'target': u'diepresse.com', 
                                   u'4': [93, 54]}, 
                u'derstandard.at': {u'1': [93, 60], u'0': [93, 62], 
                                    u'2': [93, 61], u'target': u'derstandard.at', 
                                    u'4': [93, 60]}}
        for details in WebOfTrust._format_result(data).itervalues():
            assert all(attr in details for attr in MAPPING.values())

        
if __name__ == '__main__':
    import doctest
    doctest.testmod()
    unittest.main()