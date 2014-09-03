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

	def __init__(self, api_key, username, api_url=ROOT_URL):
		
		assert(api_key)

		self.api_key = api_key
		self.api_url = api_url
		self.username = username

	def search(self, search_terms, num_results=DEFAULT_MAX_RESULTS, command = DEFAULT_COMMAND, format=DEFAULT_FORMAT):
		# Web search is by default
		search_string = ' '.join(search_terms)

		params = {'Query': search_string,
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


class Test(object):

	username = 'svitlana.vakulenko@gmail.com'
	my_account_key = 'kieVYyuW1uwvUnVo3b1+vXWtim6TuxFiYkSpPtloUhI'
	command = 'Web'
	limit = 4

	# queryBingFor = "'google fibre'"
	search_terms = ["'modul'", "'university'"]
	bs = BingSearch(my_account_key, username)
	results = bs.search(search_terms, limit, command)
	
	# pprint(results.next()) # print first
	[ pprint(res) for res in results ] #print all
	# print(len(list(results))) # number of the results

	# TODO test default api call (limit = DEFAULT_MAX_RESULTS)

	# TODO test several api access (limit > DEFAULT_MAX_RESULTS) for a common query
	#assert(len(list(results)) == limit)