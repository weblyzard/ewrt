#!/usr/bin/env python

"""
::package eWRT.ws.conceptnet
Access to conceptnet data structures using its REST interface

::author: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
"""

from json import loads

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
        return "ConceptNetNode <%s>" % (self.url)

    @staticmethod
    def lang(node_url):
        ''' ::returns: the language of the given node_url '''
        return node_url.split("/")[2]


