"""
@package eWRT.ws
Web Service access.

"""


class AbstractWebSource(object):

    ''' a raw Web Source object '''

    NAME = None

    SUPPORTED_PARAMS = None

    # a obligatory mapping, which maps results to a standard dictionary

    # or specifies a WebSourceDocument class.

    MAPPING = {'date': ('valid_from', 'convert_date'),

               'text': ('content', None),

               'title': 'title',

               }

    # MAPPING = WebSourceDocument

    def search_documents(self, search_terms, max_results=None, from_date=None, to_date=None, **kwargs):
        ''' runs the actual search / calls the webservice / API ... '''

        search_params = self._check_params(kwargs)

        raise NotImplemented

    def pre_search(self, search_params):
        ''' override this function to perform pre-run tasks '''

    def post_search(self, search_params):
        ''' override this function to perform post-run tasks '''

    @classmethod
    def _check_params(cls, params):

        search_params = {}

        for k, v in params.items():

            if k in cls.SUPPORTED_PARAMS:

                search_params[k] = v

        return search_params

    # assert all(param in cls.SUPPORTED_PARAMS for param in params)


# class AbstractIterableWebSource(AbstractWebSource):

# DEFAULT_MAX_RESULTS = None  # requires only 1 api access
#     DEFAULT_START_INDEX = 1

#     def request(self, search_term, num_results=DEFAULT_MAX_RESULTS):

#         response = self.client.execute()
#         return response

#     def search_documents(self, search_terms, max_results=None, from_date=None, to_date=None, **kwargs):
#         ''' runs the actual search / calls the webservice / API ... '''

#         search_params = self._check_params(kwargs)

#         for search_term in search_terms:

#             if (max_results > self.DEFAULT_MAX_RESULTS):
#                 count = self.DEFAULT_MAX_RESULTS
# number of reguests
#                 for i in range(self.DEFAULT_START_INDEX, max_results + 1, self.DEFAULT_MAX_RESULTS):
# detect the last iteration
#                     if (i + self.DEFAULT_MAX_RESULTS > max_results):
#                         count = max_results % self.DEFAULT_MAX_RESULTS
#                     fetched = self.request(search_term, count, index=i)

#             else:
#                 fetched = self.request(search_term, max_results)

#         raise NotImplemented

#     pass
