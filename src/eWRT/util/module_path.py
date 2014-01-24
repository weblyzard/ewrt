#!/usr/bin/env python

""" @package eWRT.util.module_path
    utils for manipulating module paths

    Examples: see unittests
"""

# (C)opyrights 2013 by Albert Weichselbraun <albert@weichselbraun.net>
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

from os.path import dirname, join

def get_resource( module_path, relative_path_list ):
    '''
    Returns the path of the given resource relative to the module's directory.

    ::param module_path: path to the given module (obtained from __file__)
    ::param relative_path_list: a string or a list of directories as used for os.path.join
    '''
    if isinstance(relative_path_list, basestring):
        relative_path_list = (relative_path_list, )
    return join(dirname(module_path), *relative_path_list)



def test_get_resource():
    ''' verifies that get_resource yields the correct resource path '''
    path = get_resource( __file__, ('resources', 'test.xml') )
    assert join(dirname(__file__), 'resources', 'test.xml') == path

def test_get_resource_single_string():
    ''' verifies that get_resource yields the correct resource path for a
        single string argument '''
    path = get_resource( __file__, 'resources/test.xml')
    assert join(dirname(__file__), 'resources', 'test.xml') == path




