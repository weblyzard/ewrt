#!/usr/bin/env python

from eWRT.util.pickleIterator import *

from tempfile import mkdtemp
from unittest import main, TestCase
from random import randint
from os.path import join

class TestPickle(TestCase):

    TESTFILE_NAME = "dump"

    def setUp(self):
        self.test_dict = [ self._get_test_dictionary(10) for x in range(10) ]
        self.fdir = mkdtemp()


    def _get_test_dictionary(self, num_elements):
        """ returns a test dictionary with the given number
            of elements """
        return dict( [ (randint(1,100), randint(1,100)) for x in range(num_elements) ] )


    def testPickle(self):
        """ tests the pickling """
        self._testPickle()
        self._testUnPickle()

    def _testUnPickle(self):
        pr = list(ReadPickleIterator( join( self.fdir, self.TESTFILE_NAME)))
        for pickled, orig in zip(pr, self.test_dict):
            self.assertEqual( pickled, orig )


    def _testPickle(self):
        """ pickles the test dictionary """

        pw = WritePickleIterator( join( self.fdir, self.TESTFILE_NAME ) )
        for element in self.test_dict:
            pw.dump(element)


if __name__ == '__main__':
    main()
