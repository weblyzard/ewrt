#!/usr/bin/env python

"""
::package eWRT.ws.conceptnet
Access to conceptnet data structures using its REST interface

::author: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
"""

from json import loads
from warnings import warn

class Node(object):

    def __init__(self, url, edges):
        self.url = url
        self.edges = [e for e in edges if e['start'] == url or e['end'] == url]

    def __hash__(self):
        ''' required to support sets '''
        return self.url.__hash__()

    def __eq__(self, other):
        ''' required to support sets '''
        return self.url == other.url

    def __repr__(self):
        return "ConceptNetNode <%s>" % (self.url.encode("utf8"))

    def specificity(self):
        ''' returns the a number that shows how specific this node is 
            e.g. (3 for "/c/en/coal" or
                  5 for "/c/en/coal/n/energy storage)
        '''
        return len(self.url.split("/"))-1

    @staticmethod
    def lang(node_url):
        ''' ::returns: the language of the given node_url '''
        lang = node_url.split("/")
        if len(lang) < 3:
            warn('Cannot extract language for node %s.' % (node_url, ))
            return ''
        return lang[2]

