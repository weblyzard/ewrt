#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@package: eWRT.ws.wordnet.tests

Convenience functions to access the NLTK WordNet interface
@author: Albert Weichselbraun
'''
from nose.tools import assert_equal

from eWRT.ws.wordnet import get_synonmys, get_antonyms, get_terms

# ------------------------------------------------------------------------------------
# Unit tests
# ------------------------------------------------------------------------------------

def test_get_antonyms():
    lemmas = get_antonyms('good') 
    assert_equal( get_terms( lemmas ), set( ('bad', 'badness', 'ill', 'evil', 'evilness') ) )
