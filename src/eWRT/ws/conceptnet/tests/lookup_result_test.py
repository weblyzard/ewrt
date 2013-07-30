#!/usr/bin/env python

from unittest import TestCase

from eWRT.ws.conceptnet.lookup_result import LookupResult
from eWRT.ws.conceptnet.util import ground_term

def test_lookup_result():
    l = LookupResult("dog")
    print l.edges

def test_concept_grounding():
    concept = ground_term('battery', ['life', 'extensive', 'too', 'short'])
    print concept
