#!/usr/bin/env python

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

    def __init__(self, cache_dir="", cache_nesting_level=0, cache_file_suffix=""):
        self.cache_dir = cache_dir
        self.cache_file_suffix = cache_file_suffix
        self.cache_nesting_level = 0

        self._cache_hit  = 0
        self._cache_miss = 0

    @staticmethod
    def getObjectId( obj_str ):
        return HASH(str)
        

    def _get_fname( self, obj_id ):
        """ computes the filename of the file with the given
            object identifier and creates the required directory
            structure (if necessary).
        """
        assert( len(obj_id) >= self.cache_nesting_level )

        obj_dir = join( *(self.cache_dir + list( obj_id[:self.cache_nesting_level] )) )
        if not exists(obj_dir):
            makedirs(obj_dir)

        return join(obj_dir, obj_id+self.cache_file_suffix)
    
    
    def fetch(self, obj_id, fetch_function):
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
            obj = fetch_function( obj_id )
            f = open(cache_file, "w")
            f.write(obj)
            f.close()
            return obj


    def getCacheStatistics(self):
        """ returns statistics regarding the cache's hit/miss ratio """
        return {'cache_hits': self._cache_hit, 'cache_misses': self._cache_miss}



class IterableCache(Cache):
    """ caches arbitrary iterable content identified by an identifier """

    def __iter__(self): return self

    def fetch(self, obj_id, fetch_function):
        """ checks whether the object with the given id exists """
        self.cache_file = self._get_fname( self.getObjectId(obj_id) )
        self.seq = 0

        if exists(self.cache_file):
            self.next = self._read_next_element()
        else:
            self._fetch_function = fetch_function(obj_id)
            self.next = self._cache_next_element()
            open( self.cache_file, "w").close()

        return self


    def _cache_next_element(self):
        """ a) retrieves the next element from the fetch function 
            b) writes the data to the cache
            c) passes the data through to the calling element
        """
        self._cache_miss += 1
        obj = self._fetch_function.next()
        f = open( "%s.%d" % (self.cache_file, self.seq), "w")
        f.write(obj)
        f.close()
        return obj


    def _read_next_element(self):
        """ returns the next element from the cache """
        self._cache_hit +=1
        try:
            obj = open( "%s.%d" % (self.cache_file, self.seq) ).read()
            self.seq += 1
            return obj
        except IOError:
            raise StopIteration



if __name__ == '__main__':
    
    from unittest import TestCase

    class TestCache(TestCase):
        """ tests the caching class based on a dummy example """

        def setUp(self):
            pass

