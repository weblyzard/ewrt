#!/usr/bin/env python

from unittest import TestCase

from eWRT.util.loggerProfile import get_file_logger
from eWRT.ws.conceptnet.lookup_result import LookupResult
from eWRT.ws.conceptnet.util import ground_term

LOGGER = get_file_logger(name='eWRT.ws.conceptnet.unittest', filename='eWRT.ws.conceptnet.unittest.log')

def test_lookup_result():
    l = LookupResult("dog")

def test_concept_grounding():
    concept = ground_term('battery', ['life', 'extensive', 'too', 'short', 'electricity'])
    LOGGER.debug("Grounded concept: %s.", concept)

