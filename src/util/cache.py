#!/usr/bin/env python

""" caches arbitrary objects """

# (C)opyrights 2008-2009 by Albert Weichselbraun <albert@weichselbraun.net>
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

__author__    = "Albert Weichselbraun"
__revision__  = "$Id$"
__copyright__ = "GPL"

from os import makedirs
from os.path import join, exists
from operator import attrgetter
from eWRT.util.pickleIterator import WritePickleIterator, ReadPickleIterator
from cPickle import dump, load

try:
    import hashutils
    HASH = hashutils.sha1
except ImportError:
    import sha
    HASH = sha.sha

class Cache(object):
    """ An abstract class for caching functions """

    def fetch(self, fetch_function, *args):
        raise NotImplementedError


class DiskCache(Cache):
    """ caches abitrary functions based on the function's arguments """

    def __init__(self, cache_dir, cache_nesting_level=0, cache_file_suffix=""):
        """ initializes the Cache object 
            @param[in] cache_dir the cache base directory
            @param[in] cache_nesting_level optional number of nesting level (0)
            @param[in] cache_file_suffix optional suffix for cache files
        """

        self.cache_dir           = cache_dir
        self.cache_file_suffix   = cache_file_suffix
        self.cache_nesting_level = cache_nesting_level

        self._cache_hit  = 0
        self._cache_miss = 0


    @staticmethod
    def getObjectId( obj_str ):
        """ returns an identifier representing the object """
        return HASH(str(obj_str)).hexdigest()
        
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
    
    def fetch(self, fetch_function, *args):
        """ fetches the object with the given id, querying
             a) the cache and
             b) the fetch_function
            if the fetch_function is called, the functions result is saved 
            in the cache 

            @param[in] function to call if the result is not in the cache
            @param[in] function arguments (used to identify, whether the function has already
                                           been cached or not)

            @returns the object (retrieved from the cache or computed)
        """
            
        cache_file = self._get_fname( self.getObjectId(args) )
        # try to fetch the object from the cache
        if exists(cache_file):
            self._cache_hit += 1
            try:
                return load(open(cache_file))
            except EOFError:
                pass

        # compute and cache it otherwise
        self._cache_miss += 1
        obj = fetch_function(*args)
        f = open(cache_file, "w")
        dump(obj, f)
        f.close()
        return obj

    def getCacheStatistics(self):
        """ returns statistics regarding the cache's hit/miss ratio """
        return {'cache_hits': self._cache_hit, 'cache_misses': self._cache_miss}


class DiskCached(DiskCache):
    """ Decorator based on Cache for caching arbitrary function calls
        usage:
          @DiskCached("./cache/myfunction")
          def myfunction(*args):
             ...
    """
    def __init__(self, cache_dir, cache_nesting_level=0, cache_file_suffix=""):
        """ initializes the Cache object 
            @param[in] fn                  the function to cache
            @param[in] cache_dir           the cache base directory
            @param[in] cache_nesting_level optional number of nesting level (0)
            @param[in] cache_file_suffix   optional suffix for cache files
        """
        DiskCache.__init__(self, cache_dir, cache_nesting_level, cache_file_suffix)
        self._fn = None

    def __call__(self, fn):
        self._fn = fn
        def wrapped_fn(*args):
            return self.fetch(self._fn, *args)
        return wrapped_fn


class MemoryCache(Cache):
    """ Cache arbitrary functions based on the function's arguments """

    def __init__(self):
        """ initializes the Cache object """
        self._cacheData = {}
        
    def fetch(self, fetch_function, *args):
        try:
            return self._cacheData[args]
        except KeyError:
            obj = fetch_function(*args)
            self._cacheData[args] = obj
            return obj

class MemoryCached(MemoryCache):
    """ Decorator based on MemoryCache for caching arbitrary function calls
        usage:
          @MemoryCached
          def myfunction(*args):
             ...
    """
    def __init__(self, fn):
        MemoryCache.__init__(self)
        self._fn = fn

    def __call__(self, *args):
        return self.fetch(self._fn, *args)


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

# $Id$
