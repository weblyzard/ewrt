'''
Created on Sep 02, 2014

:author: svakulenko
'''

# Bing API Version 2.0
# sample URL for web search https://api.datamarket.azure.com/Bing/Search/Web?$format=json&Query=%27Xbox%27&$top=2

from eWRT.ws.rest import RESTClient
from pprint import pprint

ROOT_URL = 'https://api.datamarket.azure.com/Bing/Search'
DEFAULT_FORMAT = 'json'
DEFAULT_COMMAND = 'Web' # Image, News
DEFAULT_MAX_RESULTS = 50 # requires only 1 api access
DEFAULT_START_INDEX = 1

class BingSearch(object):
	# Usage:
	# pprint(results.next())  # print first
	# [ pprint(res) for res in results ]  # print all

	def __init__(self, api_key, username, api_url=ROOT_URL):

		assert(api_key)

		self.api_key = api_key
		self.api_url = api_url
		self.username = username
		self.client = RESTClient(self.api_url, password=self.api_key, user=self.username, authentification_method='basic')

	def request(self, search_term, num_results=DEFAULT_MAX_RESULTS, command = DEFAULT_COMMAND, format=DEFAULT_FORMAT, index=DEFAULT_START_INDEX):
		''' searches Bing for the given search_term
        '''
		params = {'Query': search_term,
	  			  '$format': DEFAULT_FORMAT,
	  			  '$top': num_results}

		response = self.client.execute(command, query_parameters=params)
		return response

	def search(self, search_terms, num_results=DEFAULT_MAX_RESULTS, command = DEFAULT_COMMAND, format=DEFAULT_FORMAT, index=DEFAULT_START_INDEX):
		# Web search is by default
		for search_term in search_terms:

			if (num_results > DEFAULT_MAX_RESULTS):
				count = DEFAULT_MAX_RESULTS
				for i in range(DEFAULT_START_INDEX, num_results+1, DEFAULT_MAX_RESULTS):  # number of reguests
					if (i + DEFAULT_MAX_RESULTS > num_results):  # detect the last iteration
						count = num_results % DEFAULT_MAX_RESULTS
					fetched = self.request(search_term, count, index=i)

					for item in fetched['d']['results']:
					    try:
					        yield self.convert_item(item)
					    except Exception as e:  # ported to Python3
					        print('Error %s occured' % e)
					        continue
			else:
				fetched = self.request(search_term, num_results)

				for item in fetched['d']['results']:
				    try:
				        yield self.convert_item(item)
				    except Exception as e:  # ported to Python3
				        print('Error %s occured' % e)
				        continue

	@classmethod
	def convert_item(cls, item):
	    ''' applies a mapping to convert the result to the required format
	    '''

	    result = {'url':item['Url'],
	    		  'title': item['Title'],
	    		  }

	    return result


class TestBingSearch(object):
	# tested only Web command

	username = 'svitlana.vakulenko@gmail.com'
	my_account_key = 'kieVYyuW1uwvUnVo3b1+vXWtim6TuxFiYkSpPtloUhI'

	search_terms = ["'modul'", "'university'"]

	# test default api call (limit = DEFAULT_MAX_RESULTS)
	def test_default(self):
		bs = BingSearch(self.my_account_key, self.username)
		results = bs.search(self.search_terms)

		# assert the correct number of the results
		assert len(list(results)) == DEFAULT_MAX_RESULTS * len(self.search_terms)

	def test_smaller_limit(self):
		limit = 4
		bs = BingSearch(self.my_account_key, self.username)
		results = bs.search(self.search_terms, limit)

		# assert the correct number of the results
		assert len(list(results)) == limit * len(self.search_terms)

	def test_larger_limit(self):
		limit = 70
		bs = BingSearch(self.my_account_key, self.username)
		results = bs.search(self.search_terms, limit)

		# assert the correct number of the results
		assert len(list(results)) == limit * len(self.search_terms)