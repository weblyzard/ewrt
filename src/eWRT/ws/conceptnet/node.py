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


