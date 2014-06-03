#!/usr/bin/env python

""" pickelIterator """

# (C)opyrights 2008 by Albert Weichselbraun <albert@weichselbraun.net>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__revision__  = "$Revision"
__copyright__ = "GPL"

from cPickle import dumps, loads
from gzip import open
from binascii import b2a_base64, a2b_base64

class AbstractIterator(object):
    
    def __init__(self, fname, file_mode=None):
        self.fname = self.get_filename(fname)
        self.f = open(self.fname, file_mode) if file_mode else open(self.fname)

    def close(self):
        self.f.close()

    @classmethod
    def get_filename(cls, fname):
        return fname if fname.endswith('.gz') else fname + '.gz'

class WritePickleIterator(AbstractIterator):
    """ writes pickeled elements (available as iterator) to a file """

    def __init__(self, fname):
        AbstractIterator.__init__(self, fname, file_mode='w')

    def dump(self, obj):
        """ dumps the following object to the pickle file """
        p = b2a_base64( dumps(obj) )
        self.f.write(p)

class ReadPickleIterator(AbstractIterator):
    """ provides an iterator over pickeled elements """

    def __init__(self, fname):
        AbstractIterator.__init__(self, fname)

    def __iter__(self): 
        return self

    def next(self):
        """ returns the next pickled element in the file """
        line = self.f.readline()
        if not line:
            raise StopIteration

        return loads(a2b_base64(line))

if __name__ == '__main__':
    
    from tempfile import mkdtemp
    from unittest import main, TestCase
    from random import randint
    from os.path import join

    class TestPickle(TestCase):
        
        TESTFILE_NAME = "dump" 

        def setUp(self):
            self.test_dict = [ self._get_test_dictionary(10) for x in xrange(10) ]
            self.fdir = mkdtemp()
            

        def _get_test_dictionary(self, num_elements):
            """ returns a test dictionary with the given number 
                of elements """
            return dict( [ (randint(1,100), randint(1,100)) for x in xrange(num_elements) ] )


        def testPickle(self):
            """ tests the pickling """
            self._testPickle()
            self._testUnPickle()

        def _testUnPickle(self):
            pr = ReadPickleIterator( join( self.fdir, self.TESTFILE_NAME) )
            for pickled, orig in zip(pr, self.test_dict):
                self.assertEqual( pickled, orig )


        def _testPickle(self):
            """ pickles the test dictionary """

            pw = WritePickleIterator( join( self.fdir, self.TESTFILE_NAME ) )
            for element in self.test_dict:
                pw.dump(element)


    main()
