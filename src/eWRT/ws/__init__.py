"""
@package eWRT.ws
Web Service access.

"""


class AbstractWebSource(object):

    ''' a raw Web Source object '''

    NAME = None

    SUPPORTED_PARAMS = None

    # an obligatory mapping, which maps results to a standard dictionary

    # or specifies a WebSourceDocument class.

    MAPPING = {'date': ('valid_from', 'convert_date'),

               'text': ('content', None),

               'title': 'title',

               }

    # MAPPING = WebSourceDocument

    def search_documents(self, search_terms, max_results=None, from_date=None, to_date=None, command=None, format=None):
        ''' runs the actual search / calls the webservice / API ... '''

        raise NotImplemented

    def pre_search(self, search_params):
        ''' override this function to perform pre-run tasks '''

    def post_search(self, search_params):
        ''' override this function to perform post-run tasks '''


class AbstractIterableWebSource(AbstractWebSource):

    DEFAULT_MAX_RESULTS = None  # requires only 1 api access
    DEFAULT_COMMAND = None
    DEFAULT_FORMAT = None
    RESULT_PATH = None
    DEFAULT_START_INDEX = None

    # to be locally overriden
    def search_documents(self, search_terms, max_results=DEFAULT_MAX_RESULTS,
                         from_date=None, to_date=None, command=DEFAULT_COMMAND, format=DEFAULT_FORMAT, **kwarg):
        ''' runs the actual search / calls the webservice / API ... '''
        # Web search is by default
        fetched = self.invoke_iterator(
            search_terms, max_results, from_date, to_date, command, format)

        return self.process_json(fetched, self.RESULT_PATH)

    def invoke_iterator(self, search_terms, max_results, from_date=None, to_date=None, command=None, format=None):
        ''' runs the actual search / calls the webservice / API ... '''
        # Web search is by default
        for search_term in search_terms:

            if (max_results > self.DEFAULT_MAX_RESULTS):
                mid_results = self.DEFAULT_MAX_RESULTS
                # number of reguests
                for index in range(self.DEFAULT_START_INDEX, max_results + 1, self.DEFAULT_MAX_RESULTS):
                    # detect the last iteration
                    if (index + self.DEFAULT_MAX_RESULTS > max_results):
                        mid_results = max_results % self.DEFAULT_MAX_RESULTS
                    fetched = self.request(
                        search_term, index, mid_results, from_date, to_date, command, format)
                    yield fetched

            else:
                fetched = self.request(
                    search_term, self.DEFAULT_START_INDEX, max_results, from_date, to_date, command, format)
                yield fetched

    def process_json(self, results, json_path):
        for result in results:
            for item in json_path(result):
                try:
                    yield self.convert_item(item)
                except Exception as e:  # ported to Python3
                    print('Error %s occured' % e)
                    continue

    def request(self, search_term, current_index, max_results,
                from_date=None, to_date=None, command=None, format=None):
        ''' requests the given search_term from the API
        '''
        raise NotImplemented
