#!/usr/bin/env python

"""
::package eWRT.ws.conceptnet
Access to conceptnet data structures using its REST interface

::author: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
"""

from collections import namedtuple, Counter
from itertools import chain
from json import loads
from os.path import exists
from cPickle import load, dump

from eWRT.access.http import Retrieve
from eWRT.util.cache import DiskCached
from eWRT.ws.conceptnet.node import Node
from eWRT.ws.conceptnet.edge import Edge

CONCEPTNET_BASE_URL = 'http://conceptnet5.media.mit.edu/data/5.1'
CLEANUP_TRANSLATION_MAP = {'!': None, '.': None, '?': None, 
                           '"': None, "'": None}

Concept  = namedtuple("Concept", "language concept_name pos sense")
tokenize = lambda sentence: sentence.translate(CLEANUP_TRANSLATION_MAP).split(" ")

@DiskCached(".conceptnet-query-cache")
def retrieve_conceptnet_query_result(query):
    ''' ::param url: the url to retrieve
        ::return: the json response to the given conceptnet query
    '''
    with Retrieve(__name__) as r:
        c = r.open(query, retry=3)
        return c.read()


class Result(object):
    ''' The result of a ConceptNet query '''

    RELEVANT_VSM_ATTRIBUTES = ('endLemmas', 'startLemmas', 'text', )

    def __init__(self, json_string, min_score=1.0):
        '''
        ::param json_string: the conceptnet json string
        ::param min_score: minimum confidence score required for
                           an edge to be included.
        '''
        self.edges = [Edge(edge_dict) for edge_dict in loads(json_string)['edges']
                      if edge_dict['score'] >= min_score]

        #edge_types = load(open("known-edge-types.awi")) if exists("known-edge-types.awi") else set()
        #edge_types.update([ e['rel'] for e in self.edges ])
        #dump(edge_types, open("known-edge-types.awi","w"))

    def apply_edge_filter(self, filter_list):
        '''
        Applies the given filter to the result object
        ::param filter_list: a list containing keys and 
             potential values for these keys. The entry is filtered
             if it does not match any of the given key value pairs.
             (e.g. [('rel', '/r/isA'), ('rel', '/r/HasContext'), ...])
        '''
        self.edges = [edge for edge in self.edges if 
                      [True for key, value in filter_list
                       if edge[key] == value]]

    def apply_language_filter(self, valid_languages):
        '''
        Removes all edges where either the start or end node
        does not matches the list of valid languages
        ::param valid_languages: list of valid languages
        '''
        self.edges = [edge for edge in self.edges if
                      Node.lang(edge['start']) in valid_languages and
                      Node.lang(edge['end']) in valid_languages]

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

    def get_vsm(self, stopword_list):
        ''' 
        ::param stopword_list: an optional stopword_list to apply
        ::return: a counter object with all words and their respective
                  counts for usage in a vector space model.
        '''
        vsm = Counter()

        for attr_value in (edge[attr] for edge in self.edges for attr 
           in self.RELEVANT_VSM_ATTRIBUTES 
           if attr in edge):
            
            # handle list values
            if isinstance(attr_value, list):
                attr_value = chain(*map(tokenize, attr_value))
                vsm.update(attr_value)
            else:
                vsm.update( tokenize(attr_value) )

        # apply stopword list
        map(vsm.pop, [ s for s in stopword_list if s in vsm])
        return vsm









    
