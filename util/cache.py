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


from os import makedirs
from os.path import join, exists

class Cache(object):
    """ caches abitrary content based on an identifier """

    cache_dir = ""
    cache_file_suffix = ""

    def __init__(self, cache_dir, cache_nesting_level=0, cache_file_suffix=""):
        self.cache_dir = cache_dir
        self.cache_file_suffix = cache_file_suffix
        self.cache_nesting_level = 0


    def _get_fname( obj_id ):
        """ computes the filename of the file with the given
            object identifier and creates the required directory
            structure (if necessary).
        """
        assert( len(obj_id) >= self.cache_nesting_level )

        obj_dir = join( *(self.cache_dir + list( obj_id[:self.cache_nesting_level] )) )
        if not exists(obj_dir):
            makedirs(obj_dir)

        return join(obj_dir, obj_id+cache_file_suffix)
    
    
    def fetch(self, obj_id, fetch_function):
        """ fetches the object with the given id, querying
             a) the cache and
             b) the fetch_function
            if the fetch_function is called, the functions result is saved 
            in the cache """
            
        cache_file = self._get_fname( obj_id )
        if exists(cache_file):
            return open(cache_file).read()
        else:
            obj = fetch_function()
            f = open(cache_file, "w")
            f.write(obj)
            f.close()
            return obj

if __name__ == '__main__':
    
    from unittest import TestCase

    class TestCache(TestCase):
        """ tests the caching class based on a dummy example """

        def setUp(self):
            pass

