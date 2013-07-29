#!/usr/bin/env python

from unittest import TestCase

from eWRT.ws.conceptnet.lookup_result import LookupResult
from eWRT.access.http import Retrieve

TEST_CONCEPT = "http://conceptnet5.media.mit.edu/data/5.1/c/en/battery"

def test_lookup_result():
    with Retrieve(__name__) as r:
        c = r.open(TEST_CONCEPT)
        l = LookupResult(c.read())
        print l.edges
