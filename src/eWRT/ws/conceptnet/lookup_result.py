#!/usr/bin/env python

"""
::package eWRT.ws.conceptnet
Access to conceptnet data structures using its REST interface

::author: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
"""

from json import loads
from collections import defaultdict

from eWRT.ws.conceptnet import Concept
from eWRT.ws.conceptnet.edge import Edge


class LookupResult(Result):
    '''
    An object for handling ConceptNet search results
    '''

    @staticmethod
    def get_concept(concept_url):
        '''
        ::param concept_url: the url of the ConceptNet concept
        '''
        _, url_type, lang, concept_name, pos, sense =
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

