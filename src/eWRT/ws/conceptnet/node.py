#!/usr/bin/env python

"""
::package eWRT.ws.conceptnet
Access to conceptnet data structures using its REST interface

::author: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
"""

from json import loads

class Node(object):

    def __init__(self, json_string):
        node_dict = loads(json_string)
