#!/usr/bin/env python

""" caches arbitrary objects """

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

from os import makedirs
from os.path import join, exists
from operator import attrgetter
from eWRT.util.pickleIterator import WritePickleIterator, ReadPickleIterator

try:
    import hashutils
    HASH = hashutils.sha1
except ImportError:
    import sha
    HASH = sha.sha


class Cache(object):
    """ caches abitrary content based on an identifier """

    cache_dir = ""
    cache_file_suffix = ""

    def __init__(self, cache_dir, cache_nesting_level=0, cache_file_suffix=""):
        """ initializes the Cache object """

        self.cache_dir = cache_dir
        self.cache_file_suffix = cache_file_suffix
        self.cache_nesting_level = cache_nesting_level

        self._cache_hit  = 0
        self._cache_miss = 0


    @staticmethod
    def getObjectId( obj_str ):
        """ returns an identifier representing the object """
        return HASH(obj_str).hexdigest()
        

    def _get_fname( self, obj_id ):
        """ computes the filename of the file with the given
            object identifier and creates the required directory
            structure (if necessary).
        """
        assert( len(obj_id) >= self.cache_nesting_level )

        obj_dir = join( *( [self.cache_dir] + list( obj_id[:self.cache_nesting_level] )) )
        if not exists(obj_dir):
            makedirs(obj_dir)

        return join(obj_dir, obj_id+self.cache_file_suffix)
    
    
    def fetch(self, obj_id, fetch_function, inherited=False):
        """ fetches the object with the given id, querying
             a) the cache and
             b) the fetch_function
            if the fetch_function is called, the functions result is saved 
            in the cache """
            
        cache_file = self._get_fname( self.getObjectId(obj_id) )
        if exists(cache_file):
            self._cache_hit += 1
            return open(cache_file).read()
        else:
            self._cache_miss += 1
            if inherited:
                obj = fetch_function(self, obj_id)
            else:
                obj = fetch_function(obj_id)
            f = open(cache_file, "w")
            f.write(obj)
            f.close()
            return obj


    def getCacheStatistics(self):
        """ returns statistics regarding the cache's hit/miss ratio """
        return {'cache_hits': self._cache_hit, 'cache_misses': self._cache_miss}



class IterableCache(Cache):
    """ caches arbitrary iterable content identified by an identifier """

    _cls             = None
    _fetch_function  = None
    _cached          = False
    _pickle_iterator = None
 
    def __iter__(self): return self


    def fetch(self, obj_id, fetch_function, cls):
        """ checks whether the object with the given id exists """
        cache_file = self._get_fname( self.getObjectId(obj_id) )

        if exists(cache_file):
            self._cached = True
            self._pickle_iterator = ReadPickleIterator(cache_file)
        else:
            self._cls = cls
            self._fetch_function = fetch_function(self, obj_id)
            self._cached = False
            self._pickle_iterator = WritePickleIterator(cache_file)

        return self


    def next(self):
        if self._cached:
            return self._read_next_element()
        else:
            return self._cache_next_element()


    def _cache_next_element(self):
        """ a) retrieves the next element from the fetch function 
            b) writes the data to the cache
            c) passes the data through to the calling element
        """
        self._cache_miss += 1
        try:
            obj = attrgetter('next')(self._cls)(self)
            self._pickle_iterator.dump( obj )
            return obj
        except StopIteration:
            self._pickle_iterator.close()
            raise StopIteration


    def _read_next_element(self):
        """ returns the next element from the cache """
        self._cache_hit +=1
        try:
            return self._pickle_iterator.next()
        except IOError:
            self._pickle_iterator.close()
            raise StopIteration



if __name__ == '__main__':
    
    from unittest import TestCase

    class TestCache(TestCase):
        """ tests the caching class based on a dummy example """

        def setUp(self):
            pass

