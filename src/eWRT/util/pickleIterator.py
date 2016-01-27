#!/usr/bin/env python

''' pickelIterator '''

# (C)opyrights 2008 - 2015 by Albert Weichselbraun <albert@weichselbraun.net>
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

__copyright__ = "GPL"

import gzip
from binascii import b2a_base64, a2b_base64
try:
    from cPickle import dumps, loads
except ImportError:
    from pickle import dumps, loads

class AbstractIterator(object):
    '''
    Abstract Iterator class used to implement ReadPickleIterator
    and WritePickleIterator
    '''

    def __init__(self, fname, file_mode=None):
        self.fname = self.get_filename(fname)
        self.f = gzip.open(self.fname, file_mode) if file_mode else gzip.open(self.fname)

    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedError

    def next(self):
        ''' Python 2 compatibility '''
        return self.__next__()

    def close(self):
        self.f.close()

    @classmethod
    def get_filename(cls, fname):
        return fname if fname.endswith('.gz') else fname + '.gz'

class WritePickleIterator(AbstractIterator):
    ''' writes pickeled elements (available as iterator) to a file '''

    def __init__(self, fname):
        AbstractIterator.__init__(self, fname, file_mode='w')

    def dump(self, obj):
        ''' dumps the following object to the pickle file '''
        p = b2a_base64(dumps(obj))
        self.f.write(p)

class ReadPickleIterator(AbstractIterator):
    ''' provides an iterator over pickeled elements '''

    def __init__(self, fname):
        AbstractIterator.__init__(self, fname)

    def __iter__(self):
        return self

    def __next__(self):
        ''' returns the next pickled element in the file '''
        line = self.f.readline()
        if not line:
            raise StopIteration

        return loads(a2b_base64(line))
