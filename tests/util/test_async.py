#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import unittest

from glob import glob
from os.path import join, exists
from shutil import rmtree

from eWRT.util.async import Async


class TestAsync(unittest.TestCase):
    ''' unittests covering the class async '''

    TEST_CACHE_DIR = "./.test-async"

    def setUp(self):
        self._delCacheDir()

    def tearDown(self):
        self._delCacheDir()

    @staticmethod
    def _delCacheDir():
        if exists( TestAsync.TEST_CACHE_DIR ):
            rmtree( TestAsync.TEST_CACHE_DIR )

    def test_max_process_limit(self):
        ''' tests the max process limit '''
        async = Async(self.TEST_CACHE_DIR, max_processes=1)
        for x in xrange(2):
            async.post( [ "/bin/sleep", str(x+1) ] )

        assert async.has_processes_limit_reached() == True

        time.sleep(2)
        flag = async.has_processes_limit_reached()
        print(flag, [ p.pid for p in async.cur_processes ])
        assert flag  == False

    def test_debug_mode(self):
        ''' tests the debug mode '''
        async = Async(self.TEST_CACHE_DIR, max_processes=1, debug_dir=self.TEST_CACHE_DIR)
        for x in xrange(2):
            async.post( ["/bin/echo", "hallo"] )

        print(glob( join(self.TEST_CACHE_DIR, "debug*")))
        assert len( glob( join(self.TEST_CACHE_DIR, "debug*.out") )  ) == 2
        assert len( glob( join(self.TEST_CACHE_DIR, "debug*.err") )  ) == 2
        
if __name__ == '__main__':
    unittest.main()