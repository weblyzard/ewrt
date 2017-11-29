#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from datetime import datetime

from eWRT.ws.rss import parse

TEST_URL = "http://kurier.at/rss/channel_startseite_rss.xml"
        
class TestRss(unittest.TestCase):
    
    def test_parser(self):
        """ Test the rss module. """
        last_modified = datetime(2012,8,3,21,50,00)
        for a in parse(TEST_URL, last_modified):
            print a['link'], a['date']
            print len(a['content'])
