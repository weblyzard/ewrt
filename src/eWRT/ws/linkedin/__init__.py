#!/usr/bin/env python
# -*- coding: utf-8 -*-
import simplejson

from eWRT.ws.WebDataSource import WebDataSource

import oauth2
from atom import Link

class LinkedIn(WebDataSource):
    
    def __init__(self, consumer_key, consumer_secret, user_token, user_secret):
        WebDataSource.__init__(self)
        
        consumer = oauth2.Consumer(consumer_key, consumer_secret)
        access_token = oauth2.Token(key=user_token, secret=user_secret)
        self.client = oauth2.Client(consumer, access_token) 
        self.linkedin_uri = """http://api.linkedin.com/v1/"""
        
    def search(self, search_terms, companies=False, jobs=False, option='keywords', 
                    format='json'):
        
        '''Search linkedin for companies or jobs.
        The number of search results is limited to 10 items per search term.
        
        Usage::
        >>> linkedin_obj = LinkedIn(consumer_key, consumer_secret, user_token, user_secret)
        >>> linkedin_obj.search(['IBM', 'Microsoft'], companies=True)
        >>> linkedin_obj.search(['Python', 'Machine Learning'], jobs=True)
        
        If you need a more specific search you can use certain options instead
        of the option keywords or you place a custom search request::
        
        >>> linkedin_obj.search(['Python', 'Machine Learning'], jobs=True, option='job-title')
        >>> linkedin_obj.custom_search('http://api.linkedin.com/v1/company-search:(facets)?keywords={Python}&facets=location')
        '''
        assert isinstance(search_terms, list)
        assert not (companies and jobs) and (companies or jobs)
        
        retval = None
        
        if companies:
            retval = self.search_companies(search_terms, format)
        elif jobs:
            retval = self.search_job_by_search_terms(search_terms, format)
        
        assert retval
        return retval

    def custom_search(self, uri, format='json'):
        self._assert_basestring(uri)
        self._assert_format(format)
        
        response, content = self.client.request(uri, 
                                                headers={'x-li-format':format})
        
        return simplejson.loads(content)

    def search_company(self, search_term, option='keywords', format='json'):
        '''Search for companies using one search term'''
        self._assert_basestring(search_term, option)
        self._assert_format(format)
        
        request = self.linkedin_uri + 'company-search?%s=%s' % (option,
                                                                search_term)
        response, content = self.client.request(request, 
                                                headers={'x-li-format':format})
            
        return self._convert_json_to_dict(content, 'companies')
    
    
    def search_companies(self, search_terms, option='keywords', format='json'):
        '''Search for companies using several keywords'''
        
        assert isinstance(search_terms, list)
        self._assert_basestring(option)
        self._assert_format(format)
        
        results = []
        for search_term in search_terms:
            results.append(self.search_company(search_term, option, format))
            
        return results
    
    
    def search_job_by_search_term(self, search_term, option='keyword', format='json'):
        '''Search for a job using a certain search term'''
        
        self._assert_basestring(search_term, option)
        self._assert_format(format)
        assert isinstance(search_term, basestring)
        
        request = self.linkedin_uri + 'job-search?%s=%s' % (option, search_term)
        response, content = self.client.request(request, 
                                                headers={'x-li-format':format})
        
        return self._convert_json_to_dict(content, search_field='jobs')
    
    def search_job_by_search_terms(self, search_terms, option='keywords', 
                                            format='json'):
        '''Search for jobs using several search terms.'''
        self._assert_format(format)
        assert isinstance(search_terms, list)
        self._assert_basestring(option)
        
        results = []
        for search_term in search_terms:
            results.append(self.search_job_by_search_term(search_term, option, 
                                                          format))
        
        return results

    def _convert_json_to_dict(self, json_string, search_field):
        self._assert_basestring(json_string, search_field)
        
        raw_data = simplejson.loads(json_string)

        results = []        
        for key, value in raw_data.items():
            
            if key == search_field:
                for item in value['values']:
                    results.append(item)
        
        return results


    def _assert_format(self, format):
        assert format == 'json' or format == 'xml'
        
    def _assert_basestring(self, *args):
        for possible_string in args:
            assert isinstance(possible_string, basestring)
            assert len(possible_string) > 0
                    
