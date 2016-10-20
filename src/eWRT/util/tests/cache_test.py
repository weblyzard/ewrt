# 
# Unittests
# run nosetest from python-nose to execute these tests
#
from multiprocessing import Pool
import pytest
from shutil import rmtree

from eWRT.util.cache import *
from eWRT.util.module_path import get_resource


get_cache_dir = lambda no: get_resource(__file__, ('.unittest-temp%d' % (no), ))

class TestCached(object):
    ''' tests the MemoryCached Decorator '''
    @staticmethod
    def add(a=2, b=3): 
        return a+b

    @staticmethod
    def sub(a=2, b=3): 
        return a-b

    def testNonKeywordArguments(self):
        ''' tests the class with non Keyword Arguments '''
        for x in range(1,20):
            assert self.add(x,5) == (x+5)
            assert self.add(x,5) == (x+5)

        # test objects with a cachesize specified
        for x in range(1,20):
            assert self.sub(x,5) == x-5
            assert self.sub(x,5) == x-5
            
    def testContainsDel(self):
        ''' tests the contains and del functions '''
        d = MemoryCache()
        d.fetchObjectId("10", self.add, *(), **{'a':3, 'b':4})
        assert "10" in d
        del d["10"]
        assert "10" not in d

    def testKeywordArguments(self):
        ''' tests keyword arguments '''
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

# todo: failing
class SkipTestDiskCached(TestCached):
    @staticmethod
    @DiskCached(get_cache_dir(1))
    def add(a=1, b=2):
        return a+b

    @staticmethod
    @DiskCached(get_cache_dir(2))
    def sub(a, b):
        return a-b 
    
    def __init__(self):
       self.diskCache = DiskCache(get_cache_dir(4))

    def teardown(self):
        ''' remove the cache directories '''
        from shutil import rmtree

        for cacheDirNo in range(10):
            if exists(get_cache_dir(cacheDirNo)):
                rmtree(get_cache_dir(cacheDirNo))
        
    def testObjectKeyGeneration(self):
        ''' ensures that the diskcache object's location does not change '''
        
        CACHE_DIR = get_cache_dir(3)
        d = DiskCache(CACHE_DIR)
        getCacheLocation = lambda x: join(CACHE_DIR, Cache.getObjectId(x))
        
        d.fetchObjectId(1, str, 1)
        assert exists( getCacheLocation(1) )
        
        d.fetch(str, 2)
        assert exists( getCacheLocation( ((2,), ()) ))

    def testContains(self):
        ''' verifies that 'key' in cache works '''
        # diskcache
        assert self.diskCache.fetchObjectId(1, str, 1 ) == "1"
        
        assert 1 in self.diskCache
        assert 2 not in self.diskCache
        
        # diskcached
        assert self.add(12,14) == 26
        assert self.add.getKey(12,14) in self.add
        assert 9 not in self.add
        
    def testDelItem(self):
        ''' verifies that delitem works '''
        # diskcache
        assert self.diskCache.fetch(str, 2) == "2"
        key = self.diskCache.getKey(2)
        assert key in self.diskCache
        del self.diskCache[key]
        assert key not in self.diskCache

        # diskcached
        assert self.add(12,13) == 25
        key = self.add.getKey(12, 13)
        assert key == ((12, 13), ())
        assert key in self.add
        del self.add[key]
        assert key not in self.add     
        
    def testDirectCall(self):
        ''' tests directly calling the cache object using __call__ '''
        CACHE_DIR = get_cache_dir(4)
        cached_str = DiskCache(CACHE_DIR, fn=str)
        
        assert cached_str(7) == "7"
        assert cached_str.getKey(7) in cached_str

            
    def testIterableCache(self):
        ''' tests the iterable cache '''
        CACHE_DIR = get_cache_dir(5)
        i = IterableCache(CACHE_DIR)

        getTestIterator = lambda x: range(x)

        for iteratorSize in (4, 5, 6):
            cachedIterator = i.fetch( getTestIterator, iteratorSize )
            
            for x,y in zip(cachedIterator, getTestIterator(iteratorSize)):
                assert x == y

    @pytest.mark.slow
    def testThreadSafety(self):
        '''  tests whether everything is thread safe '''

        for a in range(1000):
            c = DiskCache(get_cache_dir(6))
            p = Pool(12)

            p.map(f, 60*[c] )
            p.map(g, 60*[c] )

            p.close()
            p.join()


def f(c):
    ''' Function for checking Diskcache with larger files.

        @remarks 
        required for the testThreadSafety unittest. 
        considers None results.
    '''
    from random import randint
    r = randint(1, 17)
    blow = lambda x: x not in (7, 8) and 100000*str(x) or None
    assert c.fetch( blow, r ) == blow(r)
    return 0

def g(c):
    ''' Function for checking DiskCache with small files.

        @remarks 
        required for the testThreadSafety unittest.
        considers None results.
    '''
 
    from random import randint
    r = randint(111, 117)
    assert c.fetch( str, r ) == str(r)
    return 0

args = {'host':'localhost', 'port':6379, 'max_cache_size': 0, 'max_cache_size': 10}
@RedisCached(args)
def dummy_function(dummy_input):
    x = 0
    for i in range(100000000):
        x = i
    print(x)
    return(x)
 
@RedisCached
def dummy_return_dict(dummy_input):
    return({'one': 1, 'two': 2})
 
class TestRedisCache():
 
    def test_int_type_preservation(self):
        x = dummy_function(1)
        assert(isinstance(x, int))
     
    def test_dict_type_preservation(self):
        d = dummy_return_dict(2)
        assert(isinstance(d, dict))
