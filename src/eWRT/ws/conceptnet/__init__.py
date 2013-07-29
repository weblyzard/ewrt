#!/usr/bin/env python

"""
::package eWRT.ws.conceptnet
Access to conceptnet data structures using its REST interface

::author: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
"""

from collections import namedtuple
from itertools import chain

Concept = namedtuple("Concept", "language concept_name pos sense")

class Result(object):
    ''' The result of a ConceptNet query '''

    def __init__(self, json_string, min_score=1.0):
        '''
        ::param json_string: the conceptnet json string
        ::param min_score: minimum confidence score required for
                           an edge to be included.
        '''
        self.edges = [Edge(edge_dict) for edge_dict in loads(json_string)
                      if edge_dict['score'] >= min_score]
        self.senses = []


    def apply_edge_filter(self, filter_dict):
        '''
        Applies the given filter to the result object
        ::param filter_dict: a dictionary containing keys and 
             potential values for these keys. The entry is filtered
             if it does not match any of the given key value pairs.
             (e.g. {'rel': '/r/isA', 'rel': '/r/HasContext', ...})
        '''
        self.edges = [edge for edge in self.edges if 
                      [True for key, value in key_value_dict.items() 
                       if edge[key] == value]]

    def get_concept(self, filter_url, include_subconcepts):
        ''' ::param filter_url: the url of the concepts to extract
            ::param include_subconcepts: whether to include subconcepts
                       (e.g. '/c/en/battery/n/the_battery_used_to_heat_the_filaments_of_a_vacuum_tube'
                             for '/c/en/battery')
        '''
        matches_filter = lambda url: url.startswith(filter_url) 
                         if include_subconcepts else lambda url: url==filter_url
        return [Concept(url, self.edges) for url in chain(
                [e['start'] for e in self.edges],
                [e['end'] for e in self.edges]) if matches_filter(url)]

