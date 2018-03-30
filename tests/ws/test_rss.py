#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from datetime import datetime

from eWRT.ws.rss import parse


TEST_URL = "https://kurier.at/xml/rss"


class TestRss(unittest.TestCase):

    def test_parser(self):
        """ Test the rss module. """
        last_modified = datetime(2012, 8, 3, 21, 50, 0)
        for a in parse(TEST_URL, last_modified):
            assert 'link' in a
            assert 'published' in a
            assert len(a['content']) > 0


if __name__ == '__main__':
    unittest.main()
