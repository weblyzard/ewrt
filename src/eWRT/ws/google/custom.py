#!/usr/bin/env python

'''
Created on Aug 30, 2014

:author: svakulenko
'''

from eWRT.ws.rest import RESTClient
from pprint import pprint

ROOT_URL = 'https://www.googleapis.com/customsearch'
DEFAULT_FORMAT = 'json'
DEFAULT_COMMAND = 'v1'
DEFAULT_MAX_RESULTS = 10  # requires only 1 api access
DEFAULT_RESULT_LANGUAGE = 'lang_de'
DEFAULT_INTERFACE_LANGUAGE = 'lang_en'
DEFAULT_START_INDEX = 1


class CustomSearch(object):
	# Usage:
	# pprint(results.next())  # print first
	# [ pprint(res) for res in results ]  # print all

	def __init__(self, api_key, engine_id, api_url=ROOT_URL):

		assert(api_key)
		self.api_key = api_key

		assert(engine_id)
		self.engine_id = engine_id

		self.api_url = api_url
		self.client = RESTClient(self.api_url, authentification_method='basic')

	def request(self, search_term, num_results=DEFAULT_MAX_RESULTS, format=DEFAULT_FORMAT, index=DEFAULT_START_INDEX):
		''' searches Google for the given search_term
        '''
		params = {'q': '"%s"' % search_term,
                  'alt': format,
                  'cx': self.engine_id,
                  'key': self.api_key,
                  'lr': DEFAULT_RESULT_LANGUAGE,
                  'hl': DEFAULT_INTERFACE_LANGUAGE,
                  'num': num_results,
                  'start': index}

		response = self.client.execute(DEFAULT_COMMAND, query_parameters=params)
		return response

	def search(self, search_terms, num_results=DEFAULT_MAX_RESULTS, format=DEFAULT_FORMAT, index=DEFAULT_START_INDEX):

		for search_term in search_terms:

			if (num_results > DEFAULT_MAX_RESULTS):
				count = DEFAULT_MAX_RESULTS
				for i in range(DEFAULT_START_INDEX, num_results+1, DEFAULT_MAX_RESULTS):  # number of reguests
					if (i + DEFAULT_MAX_RESULTS > num_results):  # detect the last iteration
						count = num_results % DEFAULT_MAX_RESULTS
					fetched = self.request(search_term, count, index=i)

					for item in fetched['items']:
					    try:
					        yield self.convert_item(item)
					    except Exception as e:  # ported to Python3
					        print('Error %s occured' % e)
					        continue
			else:
				fetched = self.request(search_term, num_results)

				for item in fetched['items']:
				    try:
				        yield self.convert_item(item)
				    except Exception as e:  # ported to Python3
				        print('Error %s occured' % e)
				        continue

	@classmethod
	def convert_item(cls, item):
	    ''' applies a mapping to convert the result to the required format
	    '''

	    result = {'url':item['link'],
	    		  'title': item['title'],
	    		  }

	    return result


class TestCustomSearch(object):

	# provide your google api key for browser applications (from Developers Console)
	my_api_key = 'AIzaSyAlXco-6Bpikl0Ji2H9NEloe4OsL-pUs2g'
	# provide your Custom search engine ID
	my_engine_id = '013438061017685574719:90y0qqxdojg' #013438061017685574719%3Aseaadr__rao

	search_terms = ["'modul'", "'university'"]

	# test default api call (limit = DEFAULT_MAX_RESULTS)
	def test_default(self, limit = DEFAULT_MAX_RESULTS):
		assert limit == DEFAULT_MAX_RESULTS

		cs_handler = CustomSearch(self.my_api_key, self.my_engine_id)
		results = cs_handler.search(self.search_terms)

		# assert the correct number of the results
		assert len(list(results)) == limit * len(self.search_terms)

	def test_smaller_limit(self, limit = 4):
		assert limit < DEFAULT_MAX_RESULTS

		cs_handler = CustomSearch(self.my_api_key, self.my_engine_id)
		results = cs_handler.search(self.search_terms, limit)

		# assert the correct number of the results
		assert len(list(results)) == limit * len(self.search_terms)

	# test several api calls (limit > DEFAULT_MAX_RESULTS)
	def test_larger_limit(self, limit = 21):
		assert limit > DEFAULT_MAX_RESULTS
		assert limit%DEFAULT_MAX_RESULTS != 0

		cs_handler = CustomSearch(self.my_api_key, self.my_engine_id)
		results = cs_handler.search(self.search_terms, limit)

		# assert the correct number of the results
		assert len(list(results)) == limit * len(self.search_terms)
