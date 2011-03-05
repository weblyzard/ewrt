#!/usr/bin/env python

""" @package eWRT.util.async
    asynchronous procedure calls 

    @warning
    this library is still a draft and might change considerable
    
"""


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

from eWRT.util.cache import DiskCache
from shutil import rmtree
from os.path import join, exists
from cPickle import load, UnpicklingError
import time
from subprocess import Popen
from glob import glob
import os
import gzip

try:
    import hashlib
    HASH = hashlib.sha1
except ImportError:
    import sha
    HASH = sha.sha


class Async(DiskCache):
    """ Asynchronous Call Handling """

    def __init__(self, cache_dir, cache_nesting_level=0, cache_file_suffix="", max_processes=8, debug_dir=None):
        """ initializes the Cache object 
            @param[in] cache_dir the cache base directory
            @param[in] cache_nesting_level optional number of nesting level (0)
            @param[in] cache_file_suffix optional suffix for cache files
            @param[in] max_processes maximum number of parallel processes
            @param[in] optional debug directory where stdout and stderr of the processes gets saved
        """

        self.cache_dir           = cache_dir
        self.cache_file_suffix   = cache_file_suffix
        self.cache_nesting_level = cache_nesting_level
        self.max_processes       = max_processes
        self.cur_processes       = []
        self.debug_dir           = debug_dir

    def getPostHashfile(self, cmd ):
        """ returns an identifier representing the object which is compatible 
            to the identifiers returned by the eWRT.util.cache.* classes. """
        args = ( tuple(cmd[1:]), ())  # required to produce the same hash as DiskCache's fetch method
        return self._get_fname( DiskCache.getObjectId( args ) ) 
        
   
    def post(self, cmd):
        """ checks whether the given command is already cached and calls
            the command otherwise.
            @param[in] cmdline command to call
            @returns the hash required to fetch this object
        """
        cache_file = self.getPostHashfile( cmd )  
        # print "I will return %s for %s." % (cache_file, " ".join(cmd) )

        # try to fetch the object from the cache
        if exists(cache_file):
            try:
                load(open(cache_file))
                return cache_file
            except (EOFError, UnpicklingError):
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

        pids = [ str(pObj.pid) for pObj in self.cur_processes ]
        return len(self.cur_processes) >= self.max_processes

    def _execute(self, cmd):
        while self.has_processes_limit_reached():
            time.sleep(5)

        if self.debug_dir:
            fname_base = join(self.debug_dir, str(time.time()) )
            stdout = open(fname_base+".out", "w")
            stderr = open(fname_base+".err", "w")
            pObj = Popen( cmd, stdout=stdout, stderr=stderr )
            os.rename( fname_base+".out", join(self.debug_dir, "debug_%d.out" % pObj.pid ))
            os.rename( fname_base+".err", join(self.debug_dir, "debug_%d.err" % pObj.pid ))
        else:
            pObj = Popen( cmd )

        # set stdout and stderr to non blocking because otherwise
        # the process will block after a limit of 64k has been reached
        # (see http://bytes.com/topic/python/answers/741393-spawning-process-subprocess)
        # fcntl(stdout, F_SETFL, fcntl(stdout, F_GETFL) | os.O_NONBLOCK)
        # fcntl(stdin, F_SETFL, fcntl(stdin, F_GETFL) | os.O_NONBLOCK)

        self.cur_processes.append( pObj )


    def fetch(self, cache_file):
        self.has_processes_limit_reached()
        while True:
            if exists(cache_file):
                try: 
                    return load( gzip.open(cache_file))
                except (EOFError, UnpicklingError) as e:
                    print "Error opening %s" % cache_file, e
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
            rmtree( TestAsync.TEST_CACHE_DIR )

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

    def testDebugMode(self):
        """ tests the debug mode """
        async = Async(self.TEST_CACHE_DIR, max_processes=1, debug_dir=self.TEST_CACHE_DIR)
        for x in xrange(2):
            async.post( ["/bin/echo", "hallo"] )

        print glob( join(self.TEST_CACHE_DIR, "debug*") )
        assert len( glob( join(self.TEST_CACHE_DIR, "debug*.out") )  ) == 2
        assert len( glob( join(self.TEST_CACHE_DIR, "debug*.err") )  ) == 2


# $Id$
