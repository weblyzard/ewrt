#!/usr/bin/env python

"""
::package eWRT.ws.conceptnet
Access to conceptnet data structures using its REST interface

::author: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
"""

from json import loads
from collections import defaultdict
from urllib import quote

from eWRT.ws.conceptnet import Concept, Result, CONCEPTNET_BASE_URL, retrieve_conceptnet_query_result

# maximum number of edges to retrieve
DEFAULT_MAX_EDGE_COUNT = 5000


class LookupResult(Result):
    '''
    An object for handling ConceptNet search results
    '''
    def __init__(self, term=None, rel_type='c', lang='en', pos_tag = None, conceptnet_url=None, strict=False, count=DEFAULT_MAX_EDGE_COUNT):
        '''
        ::param term: the lookup term
        ::param rel_type: the relation type (c).
        ::param lang: the language to use (en).
        ::param pos_tag: an optional lookup pos_tag
        ::param conceptnet_url: 
        ::param strict: if set remove all edges that do not contain the
                        exact conceptnet_url
        ::param count: maximum number of edges to retrieve
        ::return: a list of edges matching the lookup query
        '''
        if not conceptnet_url:
            conceptnet_url  = "%s/%s/%s/%s" % (CONCEPTNET_BASE_URL, rel_type, lang, term)
        host, url = conceptnet_url.split("/", 3)[2:]
        conceptnet_url = "http://%s/%s?limit=%d" % (host, quote(url), count)

        Result.__init__(self, retrieve_conceptnet_query_result(conceptnet_url))

    @staticmethod
    def get_concept_from_url(concept_url):
        '''
        ::param concept_url: the url of the ConceptNet concept
        '''
        _, url_type, lang, concept_name, pos, sense = \
            self._split(concept_url, '/', 6)
        return Concept(lang, concept_name, pos, sense)


    @staticmethod
    def _split(s, delimiter, size):
        '''
        ::param s: the string to split
        ::param delimiter: delimiter
        ::param size: size of the list to return
        '''
        l = s.split(delimiter, size)
        return l + (size - len(l)) * [None]


if __name__ == '__main__':
    r = LookupResult('lord', strict=True)
    from eWRT.ws.conceptnet.util import VALID_SENSE_FILTER, VALID_LANGUAGES
    r.apply_language_filter(VALID_LANGUAGES)
    #r.apply_edge_filter(VALID_SENSE_FILTER)
    #print "\n".join(map(repr, r.get_senses())) 
    print r.get_vsm(stopword_list=())
