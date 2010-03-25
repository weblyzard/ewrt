#!/usr/bin/env python

""" caches arbitrary objects """

# (C)opyrights 2008-2010 by Albert Weichselbraun <albert@weichselbraun.net>
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

from os import makedirs, remove
from os.path import join, exists
from eWRT.util.pickleIterator import WritePickleIterator, ReadPickleIterator
from cPickle import dump, load
from time import time
from operator import itemgetter
from hashlib import sha1 

class Cache(object):
    """ An abstract class for caching functions """
    
    def __init__(self, fn=None):
        self.fn = fn
    
    def __call__(self, *args, **kargs):
        """ retrieves the result using self.fn as function and
            the cache.
            @param[in] args     arguments
            @param[in] kargs    optional keyword arguments
        """
        assert self.fn
        return self.fetch(self.fn, *args, **kargs)

    def fetchObjectId(self, key, fetch_function, *args, **kargs):
        """ Fetches a object from the cache or computes it by calling the 
            fetch_function.
            The key helps to determine whether the object is already in
            the cache or not. 
        """
        raise NotImplementedError

    def fetch(self, fetch_function, *args, **kargs):
        """ Fetches a object from the cache or computes it by calling the 
            fetch_function.
            The objectId is computed based on the function arguments
        """
        raise NotImplementedError

    @staticmethod
    def getKey( *args, **kargs):
        """ returns the key for a set of function parameters """
        return (args, tuple(kargs.items()) )

    @staticmethod
    def getObjectId( obj ):
        """ returns an identifier representing the object """
        return sha1(str( obj )).hexdigest()



class DiskCache(Cache):
    """ caches abitrary functions based on the function's arguments """

    def __init__(self, cache_dir, cache_nesting_level=0, cache_file_suffix="", fn=None):
        """ initializes the Cache object 
            @param[in] cache_dir the cache base directory
            @param[in] cache_nesting_level optional number of nesting level (0)
            @param[in] cache_file_suffix optional suffix for cache files
            @param[in] fn function to cache (optional; required for directly calling the class
                          using __call__
        """
        Cache.__init__(self, fn)
        self.cache_dir           = cache_dir
        self.cache_file_suffix   = cache_file_suffix
        self.cache_nesting_level = cache_nesting_level

        self._cache_hit  = 0
        self._cache_miss = 0      
        
    def fetch(self, fetch_function, *args, **kargs):
        """ fetches the object with the given id, querying
             a) the cache and
             b) the fetch_function
            if the fetch_function is called, the functions result is saved 
            in the cache 

            @param[in] function to call if the result is not in the cache
            @param[in] args   arguments 
            @param[in] kargs  optional keyword arguments

            @returns the object (retrieved from the cache or computed)
        """
        objectId = self.getKey(*args, **kargs) 
        return self.fetchObjectId(objectId, fetch_function, *args, **kargs)

    def __contains__(self, key):
        """ returns whether the key is already stored in the cache """
        cache_file = self._get_fname( self.getObjectId(key)  ) 
        return exists(cache_file)
    
    def __delitem__(self, key):
        """ removes the given item from the cache """
        cache_file = self._get_fname( self.getObjectId(key)  )
        remove( cache_file )
        
    
    def fetchObjectId(self, key, fetch_function, *args, **kargs):
        """ fetches the object with the given id, querying
             a) the cache and
             b) the fetch_function
            if the fetch_function is called, the functions result is saved 
            in the cache 

            @param[in] key      key to fetch
            @param[in] function to call if the result is not in the cache
            @param[in] args     arguments 
            @param[in] kargs    optional keyword arguments

            @returns the object (retrieved from the cache or computed)
        """
        cache_file = self._get_fname( self.getObjectId(key)  ) 
        # try to fetch the object from the cache
        if exists(cache_file):
            self._cache_hit += 1
            try:
                return load(open(cache_file))
            except EOFError:
                pass

        # compute and cache it otherwise
        self._cache_miss += 1
        obj = fetch_function(*args, **kargs)
        if obj != None:
            f = open(cache_file, "w")
            dump(obj, f)
            f.close()
        return obj

    def getCacheStatistics(self):
        """ returns statistics regarding the cache's hit/miss ratio """
        return {'cache_hits': self._cache_hit, 'cache_misses': self._cache_miss}

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
 

class DiskCached():
    """ Decorator based on Cache for caching arbitrary function calls
        usage:
          @DiskCached("./cache/myfunction")
          def myfunction(*args):
             ...
    """
    __slots__ = ('cache', )
    
    def __init__(self, cache_dir, cache_nesting_level=0, cache_file_suffix=""):
        """ initializes the Cache object 
            @param[in] fn                  the function to cache
            @param[in] cache_dir           the cache base directory
            @param[in] cache_nesting_level optional number of nesting level (0)
            @param[in] cache_file_suffix   optional suffix for cache files
        """
        self.cache = DiskCache(cache_dir, cache_nesting_level, cache_file_suffix)

    def __call__(self, fn):
        self.cache.fn = fn 
        return self.cache


class MemoryCache(Cache):
    """ Cache arbitrary functions based on the function's arguments """

    __slots__ = ('max_cache_size', '_cacheData', '_usage' )

    def __init__(self, max_cache_size =0, fn=None):
        """ initializes the Cache object """
        Cache.__init__(self, fn)
        self._cacheData  = {}  
        self._usage      = {}
        self.max_cache_size = max_cache_size

    def fetch(self, fetch_function, *args, **kargs):
        key = self.getKey(*args, **kargs) 
        return self.fetchObjectId(key, fetch_function, *args, **kargs)
        
    def fetchObjectId(self, key, fetch_function, *args, **kargs):
        # update the object's last usage time stamp
        self._usage[key]     = time()  
        try:
            return self._cacheData[key]
        except KeyError:
            obj = fetch_function(*args, **kargs)
            if obj != None:
                self.garbage_collect_cache()
                self._cacheData[key] = obj
            return obj

    def garbage_collect_cache(self):
        """ removes the object which have not been in use for the 
            longest time """
        if self.max_cache_size == 0 or len(self._cacheData)<=self.max_cache_size: 
            return

        (key, _) = sorted( self._usage.items(), key=itemgetter(1), reverse=True ).pop()
        del self._usage[key]
        del self._cacheData[key]


class MemoryCached(MemoryCache):
    """ Decorator based on MemoryCache for caching arbitrary function calls
        usage:
          @MemoryCached or @MemoryCached(max_cache_size)
          def myfunction(*args):
             ...
    """
    def __init__(self, arg):
        """ initializes the MemoryCache object 
            @param[in] either the max_cache_size or the function to call
        """
        if hasattr(arg, '__call__'):
            MemoryCache.__init__(self)
            self._fn = arg
        else:
            MemoryCache.__init__(self, max_cache_size=arg)
            self._fn = None

    def __call__(self, *args, **kargs):
        if self._fn == None:
            fn = args[0]
            def wrapped_fn(*args, **kargs):
                return self.fetch(fn, *args, **kargs)
            return wrapped_fn
        else:
            return self.fetch(self._fn, *args, **kargs)


class IterableCache(DiskCache):
    """ caches arbitrary iterable content identified by an identifier """

    def __iter__(self): return self

    def fetchObjectId(self, key, function, *args, **kargs):
        """ fetches the object with the given id, querying
             a) the cache and
             b) the function
            if the function is called, the functions result is saved 
            in the cache 

            @param[in] key      key to fetch
            @param[in] function to call if the result is not in the cache
            @param[in] args     arguments 
            @param[in] kargs    optional keyword arguments

            @returns the object (retrieved from the cache or computed)
        """
        cache_file = self._get_fname( self.getObjectId(key)  )

        if exists(cache_file):
            self._cached = True
            self._pickle_iterator = ReadPickleIterator(cache_file)
        else:
            self._fetch_function_iterator = function(*args, **kargs).__iter__()
            self._cached = False
            self._pickle_iterator = WritePickleIterator(cache_file)

        return self


    def next(self):
        return self._read_next_element() if self._cached else self._cache_next_element()

    def _cache_next_element(self):
        """ a) retrieves the next element from the fetch function 
            b) writes the data to the cache
            c) passes the data through to the calling element
        """
        self._cache_miss += 1
        try:
            obj = self._fetch_function_iterator.next()
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


# 
# Unittests
# run nosetest from python-nose to execute these tests
#

class TestCached(object):
    """ tests the MemoryCached Decorator """
    @staticmethod
    def add(a=2,b=3): 
        return a+b

    @staticmethod
    def sub(a=2,b=3): 
        return a-b

    def testNonKeywordArguments(self):
        """ tests the class with non Keyword Arguments """
        for x in xrange(1,20):
            assert self.add(x,5) == (x+5)
            assert self.add(x,5) == (x+5)

        # test objects with a cachesize specified
        for x in xrange(1,20):
            assert self.sub(x,5) == x-5
            assert self.sub(x,5) == x-5

    def testKeywordArguments(self):
        """ tests keyword arguments """
        assert self.add(3, b=7) == 3+7
        assert self.add(3, b=7) == 3+7
        assert self.add(a=9, b=8) == 9+8
        

class TestMemoryCached(TestCached):
    @staticmethod
    @MemoryCached
    def add(a=1, b=2):
        return a+b

    @staticmethod
    @MemoryCached(12)
    def sub(a=2, b=1):
        return a-b 

class TestDiskCached(TestCached):
    @staticmethod
    @DiskCached("./.unittest-temp1")
    def add(a=1, b=2):
        return a+b

    @staticmethod
    @DiskCached("./.unittest-temp2")
    def sub(a, b):
        return a-b 
    
    def __init__(self):
        self.diskCache = DiskCache("./unittest-temp4")

    def teardown(self):
        """ remove the cache directories """
        from shutil import rmtree

        for cacheDirNo in range(6):
            if exists("./.unittest-temp%d" % cacheDirNo):
                rmtree("./.unittest-temp%d" % cacheDirNo)
        
    def testObjectKeyGeneration(self):
        """ ensures that the diskcache object's location does not change """
        
        CACHE_DIR = "./.unittest-temp3"
        d = DiskCache(CACHE_DIR)
        getCacheLocation = lambda x: join(CACHE_DIR, Cache.getObjectId(x))
        
        d.fetchObjectId(1, str, 1)
        assert exists( getCacheLocation(1) )
        
        d.fetch(str, 2)
        assert exists( getCacheLocation( ((2,), ()) ))

    def testContains(self):
        """ verifies that 'key' in cache works """
        # diskcache
        assert self.diskCache.fetchObjectId(1, str, 1 ) == "1"
        
        assert 1 in self.diskCache
        assert 2 not in self.diskCache
        
        # diskcached
        assert self.add(12,14) == 26
        assert self.add.getKey(12,14) in self.add
        assert 9 not in self.add
        
    def testDelItem(self):
        """ verifies that delitem works """
        # diskcache
        assert self.diskCache.fetch(str, 2) == "2"
        key = self.diskCache.getKey(2)
        assert key in self.diskCache
        del self.diskCache[key]
        assert key not in self.diskCache

        # diskcached
        assert self.add(12,13) == 25
        key = self.add.getKey(12,13)
        assert key == ((12,13), ())
        assert key in self.add
        del self.add[key]
        assert key not in self.add     
        
    def testDirectCall(self):
        """ tests directly calling the cache object using __call__ """
        CACHE_DIR = "./.unittest-temp4"
        cached_str = DiskCache(CACHE_DIR, fn=str)
        
        assert cached_str(7) == "7"
        assert cached_str.getKey(7) in cached_str

            
    def testIterableCache(self):
        """ tests the iterable cache """
        CACHE_DIR = "./.unittest-temp5"        
        i = IterableCache(CACHE_DIR)

        getTestIterator = lambda x: xrange(x)

        for iteratorSize in (4,5,6):
            cachedIterator = i.fetch( getTestIterator, iteratorSize )
            
            for x,y in zip(cachedIterator, getTestIterator(iteratorSize)):
                print x,y
                assert x == y
                           
# $Id$
