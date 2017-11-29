#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Nov 29, 2017

.. codeauthor: max goebel <mcgoebel@gmail.com>
'''
import unittest

from nose.plugins.attrib import attr

from eWRT.ws.wikipedia.descriptor import WikiPedia

class TestDescriptor(unittest.TestCase):
    """ tests the http class """
    
    TEST_TERMS = { 
                   None: ('noresults_ksfdasdf', ),
                   'Wolfgang Amadeus Mozart': ( 'wolfgang amadeus', 'mozart', ), 
                   'Pope Benedict XVI': ('pope benedict xvi', 'joseph ratzinger', ),
                 }

    @attr("remote")
    def test_descriptor(self):
        """ tries to retrieve the following url's from the list """

        d = WikiPedia()
        for descriptor, synonyms in self.TEST_TERMS.iteritems():
            for synonym in synonyms:
                print synonym, d.getDescriptor(synonym)
                assert descriptor == d.getDescriptor(synonym)