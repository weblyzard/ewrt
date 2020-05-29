#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on May 29, 2020

@author: jakob <jakob.steixner@modul.ac.at>
'''
import time
import datetime
import unittest
import mock

from eWRT.util.cache import TTLMemoryCached

class TestTTLMemoryCached(unittest.TestCase):

    def test_fast_expiry(self):

        fn = mock.MagicMock(return_value=1)

        @TTLMemoryCached(ttl=datetime.timedelta(milliseconds=1))
        def dummy_fast_expiry():
            fn()

        dummy_fast_expiry()
        time.sleep(0.1)
        dummy_fast_expiry()
        assert fn.call_count == 2

    def test_slow_expiry(self):

        fn = mock.MagicMock(return_value=1)
        @TTLMemoryCached(ttl=datetime.timedelta(days=1))
        def dummy_slow_expiry():
            return fn()

        dummy_slow_expiry()
        time.sleep(0.1)
        dummy_slow_expiry()
        assert fn.call_count == 1


