#!/usr/bin/env python

""" @package eWRT.util.async
    asynchronous procedure calls 

    WARNING: this library is still a draft and might change considerable
    
"""


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

from os import makedirs, removedirs
from os.path import join, exists
from cPickle import load
import time
from subprocess import Popen
import os

try:
    import hashlib
    HASH = hashlib.sha1
except ImportError:
    import sha
    HASH = sha.sha


class Async(object):
    """ Asynchronous Call Handling """

    def __init__(self, cache_dir, cache_nesting_level=0, cache_file_suffix="", max_processes=8):
        """ initializes the Cache object 
            @param[in] cache_dir the cache base directory
            @param[in] cache_nesting_level optional number of nesting level (0)
            @param[in] cache_file_suffix optional suffix for cache files
            @param[in] max_processes maximum number of parallel processes
        """

        self.cache_dir           = cache_dir
        self.cache_file_suffix   = cache_file_suffix
        self.cache_nesting_level = cache_nesting_level
        self.max_processes       = max_processes
        self.cur_processes       = []

    @staticmethod
    def getObjectId( obj ):
        """ returns an identifier representing the object which is compatible 
            to the identifiers returned by the eWRT.util.cache.* classes. """
        obj = ( tuple(obj[1:]), () )
        return HASH(str( obj )).hexdigest()
        
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

    
    def post(self, cmd):
        """ checks whether the given command is already cached and calls
            the command otherwise.
            @param[in] cmdline command to call
            @returns the hash required to fetch this object
        """
        cache_file = self._get_fname( self.getObjectId( cmd  ))  
        # try to fetch the object from the cache
        if exists(cache_file):
            try:
                load(open(cache_file))
                return cache_file
            except EOFError:
                pass

        self._execute(cmd)
        return cache_file

    def has_processes_limit_reached(self):
        """ closes finished processes and verifies whether we have already 
            reached the maximum number of processes """
        # verify whether all registered processes are still running
        for pObj in self.cur_processes:
            if pObj.poll()!=None:
               self.cur_processes.remove( pObj )

        return len(self.cur_processes) >= self.max_processes

    def _execute(self, cmd):
        while self.has_processes_limit_reached():
            time.sleep(2)
        pObj = Popen( cmd )
        self.cur_processes.append( pObj )


    def fetch(self, cache_file):
        self.has_processes_limit_reached()
        while True:
            if exists(cache_file):
                try: 
                    return load(open(cache_file))
                except EOFError:
                    pass

            time.sleep(10)


class TestAsync(object):
    """ unittests covering the class async """

    TEST_CACHE_DIR = "./.test-async"

    def setUp(self):
        self._delCacheDir()

    def tearDown(self):
        self._delCacheDir()

    @staticmethod
    def _delCacheDir():
        if exists( TestAsync.TEST_CACHE_DIR ):
            os.removedirs( TestAsync.TEST_CACHE_DIR )

    def testMaxProcessLimit(self):
        """ tests the max process limit """
        async = Async(self.TEST_CACHE_DIR, max_processes=1)
        for x in xrange(2):
            async.post( [ "/bin/sleep", str(x+1) ] )

        assert async.has_processes_limit_reached() == True

        time.sleep(2)
        flag = async.has_processes_limit_reached()
        print flag, [ p.pid for p in async.cur_processes ]
        assert flag  == False

# $Id$
