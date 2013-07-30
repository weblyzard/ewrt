#!/usr/bin/env python

"""
::package eWRT.ws.conceptnet
Access to conceptnet data structures using its REST interface

::author: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
"""

from collections import namedtuple, Counter
from itertools import chain
from json import loads

from eWRT.access.http import Retrieve
from eWRT.util.cache import DiskCached
from eWRT.ws.conceptnet.node import Node
from eWRT.ws.conceptnet.edge import Edge

CONCEPTNET_BASE_URL = 'http://conceptnet5.media.mit.edu/data/5.1'

Concept = namedtuple("Concept", "language concept_name pos sense")


@DiskCached(".conceptnet-query-cache")
def retrieve_conceptnet_query_result(query):
    ''' ::param url: the url to retrieve
        ::return: the json response to the given conceptnet query
    '''
    with Retrieve(__name__) as r:
        c = r.open(query)
        return c.read()


class Result(object):
    ''' The result of a ConceptNet query '''

    RELEVANT_VSM_ATTRIBUTES = ('endLemmas', 'startlemmas', 'text', )

    def __init__(self, json_string, min_score=1.0):
        '''
        ::param json_string: the conceptnet json string
        ::param min_score: minimum confidence score required for
                           an edge to be included.
        '''
        self.edges = [Edge(edge_dict) for edge_dict in loads(json_string)['edges']
                      if edge_dict['score'] >= min_score]

    def apply_edge_filter(self, filter_dict):
        '''
        Applies the given filter to the result object
        ::param filter_dict: a dictionary containing keys and 
             potential values for these keys. The entry is filtered
             if it does not match any of the given key value pairs.
             (e.g. {'rel': '/r/isA', 'rel': '/r/HasContext', ...})
        '''
        self.edges = [edge for edge in self.edges if 
                      [True for key, value in filter_dict.items() 
                       if edge[key] == value]]

    def get_concept(self, filter_url=None, include_subconcepts=False):
        ''' ::param filter_url: an optional filter_url for the concepts to extract 
            ::param include_subconcepts: whether to include subconcepts, if filtering
                       is enabled.
                       (e.g. '/c/en/battery/n/the_battery_used_to_heat_the_filaments_of_a_vacuum_tube'
                             for '/c/en/battery')
        '''
        matches_filter = lambda url: url.startswith(filter_url) if \
                            include_subconcepts else lambda url: url==filter_url

        return [Node(url, self.edges) for url in chain(
                [e['start'] for e in self.edges],
                [e['end'] for e in self.edges]) 
                if not filter_url or matches_filter(url)]

    def get_senses(self):
        ''' ::return: the set of senses present in the result '''
        return set(self.get_concept())

    def get_vsm(self):
        ''' 
        ::return: a counter object with all words and their respective
                  counts for usage in a vector space model.
        '''
        vsm = Counter()

        for attr_value in (edge[attr] for edge in self.edges for attr 
           in self.RELEVANT_VSM_ATTRIBUTES 
           if attr in edge):
            
            # handle list values
            if isinstance(attr_value, list):
                map(vsm.update, attr_value)
            else:
                vsm.update(attr_value)

        return vsm









    
