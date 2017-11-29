#!/usr/bin/env python
import unittest

from nose.plugins.attrib import attr


class TestWikiDistance(unittest.TestCase):
    
    def __init__(self):
        self.wd = WikiDistance()
        
    @attr("db")
    def test_same_as(self):
        """ tests the sameAs method """
        assert self.wd.isSameAs("cpu", "central processing unit")
        assert not self.wd.isSameAs("cpu", "desk")

    @attr("db")
    def test_is_sibling(self):
        """ tests whether terms are siblings """
        assert self.wd.isSibling("swimming (sport)", "front crawl")
        assert self.wd.isSibling("swimming (sport)", "butterfly stroke")
        assert not self.wd.isSibling("cpu", "front crawl")
 
    @attr("db")
    def test_term_pairs(self):
        """ test specific term pairs"""
        assert self.wd.isSibling("design area", "risk") == False

    @staticmethod
    @attr("db")
    def test_multiprocessing(self):
        """ tests the multi processing capabilities of this module """
        from multiprocessing import Pool
        p = Pool(4)
        res = p.map(p_isSibling, [('cpu', 'desk'), ('cpu', 'central processing unit'),
                                  ('austria', 'carinthia'), ('linux', 'bsd'),
                                  ('microsoft', 'microsoft inc.'), ('anna', 'ana') ]
                                 )
        assert [ same for same, _ in res ] == [ False, True, False, False, True, False ]

    @attr("db")
    def test_connection_limit(self):
        for _ in xrange(300):
            assert self.wd.isSameAs("design area", "risk") == False