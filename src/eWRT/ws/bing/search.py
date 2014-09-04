'''
Created on Sep 02, 2014

:author: svakulenko
'''

# Bing API Version 2.0
# sample URL for web search https://api.datamarket.azure.com/Bing/Search/Web?$format=json&Query=%27Xbox%27

from eWRT.ws.rest import RESTClient
from pprint import pprint

ROOT_URL = 'https://api.datamarket.azure.com/Bing/Search'
DEFAULT_FORMAT = 'json'
DEFAULT_COMMAND = 'Web' # Image, News
DEFAULT_MAX_RESULTS = 50 # requires only 1 api access

class BingSearch(object):
	# Usage:
	# pprint(results.next())  # print first
	# [ pprint(res) for res in results ]  # print all

	def __init__(self, api_key, username, api_url=ROOT_URL):

		assert(api_key)

		self.api_key = api_key
		self.api_url = api_url
		self.username = username

	def search(self, search_terms, num_results=DEFAULT_MAX_RESULTS, command = DEFAULT_COMMAND, format=DEFAULT_FORMAT):
		# Web search is by default
		for search_term in search_terms:
			params = {'Query': search_term,
		  			  '$format': DEFAULT_FORMAT,
		  			  '$top': num_results}

			r = RESTClient(self.api_url, password=self.api_key, user=self.username, authentification_method='basic')
			fetched = r.execute(command, query_parameters=params)

			for item in fetched['d']['results']:
			    try:
			        yield self.convert_item(item)
			    except Exception as e:
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

	def test_larger_limit(self):  # fails
		limit = 70
		bs = BingSearch(self.my_account_key, self.username)
		results = bs.search(self.search_terms, limit)

		# assert the correct number of the results
		assert len(list(results)) == limit * len(self.search_terms)