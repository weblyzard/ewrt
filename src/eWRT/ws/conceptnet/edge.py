#!/usr/bin/env python

"""
::package eWRT.ws.conceptnet
Access to conceptnet data structures using its REST interface

::author: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
"""

class Edge(dict):
    '''
    A ConceptNet edge.
    '''
    def __init__(self, edge_dict):
        '''
        ::param edge_dict: a dictionary used to initialize the edge
        '''
        dict.__init__(self)
        self.update(edge_dict)

### IMPORTANT: block antonyms and scores with negative values
### NLP is not yet ready to handle them

