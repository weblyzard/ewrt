#!/usr/bin/env python

""" @package eWRT.util.assert
    Assertion based counters 

    Examples: see unittests
"""

# (C)opyrights 2011 by Albert Weichselbraun <albert@weichselbraun.net>
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

from time import time
from unittest import TestCase

class AssertReturnValue(object):
    """ decorator class used to time functions """

    def __init__(self):
        pass

    def assertReturnValue(self, x):
        x = f(*args, **kwargs)
        assert eval(condition)
        return x


class TimedTest(TestCase):

    @assertReturnValue("int(x)>12", "countPassed", "countFailed")
    def testAssertReturnValue(object):
         return 24
