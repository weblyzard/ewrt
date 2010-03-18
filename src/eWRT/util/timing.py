#!/usr/bin/env python

""" @package eWRT.util.timing
    timing of abitrary method calls

    Examples: see unittests
"""

# (C)opyrights 2010 by Albert Weichselbraun <albert@weichselbraun.net>
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

class Timed(object):
    """ decorator class used to time functions """

    def __init__(self, f):
       self.f = f
       self.clear()

    def __call__(self, *args, **kargs):
        """ calls the timed function and computes all necessary
            statistics """
        self.numberOfCalls += 1
        beforeCall= time()
        retVal = self.f(*args, **kargs)
        self.lastCallDuration   = time()-beforeCall
        self.totalCallDuration += self.lastCallDuration
        return retVal

    def clear(self):
        self.startTime         = time()
        self.lastCallDuration  = None
        self.totalCallDuration = 0.
        self.numberOfCalls     = 0
 

class TimedTest(TestCase):

    @Timed
    def _timeFunction(self, a, b):
        [ x for x in xrange(1000) ]
        return a + b

    def testReturnValue(self):
        print self._timeFunction(self, 2,8)
        assert self._timeFunction(self, 2, 8) == 10

    def testCallStatistics(self):
        NR_CALL = 5000
        for x in xrange(NR_CALL):
            self._timeFunction(self, x, 10*x)
        
        assert self._timeFunction.numberOfCalls == NR_CALL
        self.assertAlmostEqual( self._timeFunction.totalCallDuration/NR_CALL, self._timeFunction.lastCallDuration, 1 )
        
    def testClearCallStatistics(self):
        NR_CALL = 5000
        for x in xrange(NR_CALL):
            self._timeFunction(self, x, 10*x)

        self._timeFunction.clear()
        assert self._timeFunction.totalCallDuration == 0.
        assert self._timeFunction.numberOfCalls == 0
        



        
# $Id$
