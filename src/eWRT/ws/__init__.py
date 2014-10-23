"""
@package eWRT.ws
Web Service access.

"""


class AbstractWebSource(object):

    """a raw Web Source object"""

    NAME = None
    SUPPORTED_PARAMS = None

    # an obligatory mapping, which maps results to a standard dictionary
    # or specifies a WebSourceDocument class.
    MAPPING = None
    # MAPPING = WebSourceDocument

    def search_documents(self, search_terms, max_results=None, from_date=None,
                         to_date=None, **kwargs):
        """runs the actual search / calls the webservice / API ..."""

        raise NotImplemented

    def pre_search(self, search_params):
        """override this function to perform pre-run tasks"""

    def post_search(self, search_params):
        """override this function to perform post-run tasks"""


class AbstractIterableWebSource(AbstractWebSource):

    """web source implementing several calls to the API
    iterating over search terms and over API-specific
    maximal number of results restriction
    """

    DEFAULT_MAX_RESULTS = None  # requires only 1 api access
    DEFAULT_COMMAND = None
    DEFAULT_FORMAT = None
    RESULT_PATH = None
    DEFAULT_START_INDEX = None

    # to be locally overriden
    def search_documents(self, search_terms, max_results=DEFAULT_MAX_RESULTS,
                         from_date=None, to_date=None, **kwargs):
        """calls iterator and results' post-processor"""

        fetched = self.invoke_iterator(
            search_terms, max_results, from_date, to_date, **kwargs)

        return self.process_output(fetched, self.RESULT_PATH)

    def invoke_iterator(self, search_terms, max_results, from_date=None,
                        to_date=None, command=None, output_format=None):
        """iterator: iterates over search terms and API requests"""

        for search_term in ["'{0}'".format(t) for t in search_terms]:

            if (max_results > self.DEFAULT_MAX_RESULTS):
                mid_results = self.DEFAULT_MAX_RESULTS
                # number of reguests
                for index in range(self.DEFAULT_START_INDEX,
                                   max_results + 1, self.DEFAULT_MAX_RESULTS):
                    # detect the last iteration
                    if (index + self.DEFAULT_MAX_RESULTS > max_results):
                        mid_results = max_results % self.DEFAULT_MAX_RESULTS
                    fetched = self.request(search_term, index, mid_results,
                                           from_date, to_date, command,
                                           output_format)
                    yield fetched

            else:
                fetched = self.request(
                    search_term, self.DEFAULT_START_INDEX, max_results,
                    from_date, to_date, command, output_format)
                yield fetched

    def process_output(self, results, path):
        """results' post-processor: iterates over the API responses
        and calls the output convertor
        """

        for result in results:
            for item in path(result):
                try:
                    yield self.convert_item(item)
                except Exception as e:  # ported to Python3
                    print('Error %s occured' % e)
                    continue

    def request(self, search_term, current_index, max_results,
                from_date=None, to_date=None, command=None,
                output_format=None):
        """calls the web source's API
        """
        
        raise NotImplemented
