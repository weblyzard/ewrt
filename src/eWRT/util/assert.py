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
from collections import Counter

class AssertReturnValue(object):
    """ decorator class used to time functions """

    def __init__(self, evalExpression, counterNameTrue, counterNameFalse):
        """
        @param evalExpression: the expression to verify (e.g. x>12); 
        @note evalExpression uses the variable x for the return value
        @param counterNameTrue: counter to increase if the condition is true
        @param counterNameFalse:counter to increase if the condition is false  
        """
        self.fn               = None
        self.evalExpression = evalExpression
        self.counterNameTrue = counterNameTrue
        self.counterNameFalse = counterNameFalse
        self.counter          = Counter()
        
    def _assertReturnValue(self, x):
        if eval(self.evalExpression):
            self.counter[self.counterNameTrue] += 1
        else:
            self.counter[self.counterNameFalse] += 1

    def __call__(self, fn):
        """
        returns the wrapper object which is called instead of the original
        function ones the decorator is used.
        """
        def wrapper(*fargs, **kw):
            returnValue = self.fn(*fargs, **kw) 
            self._assertReturnValue(returnValue)
            return returnValue

        # Save wrapped function reference
        self.fn = fn
        wrapper.__name__ = fn.__name__
        wrapper.__dict__.update(fn.__dict__)
        wrapper.__doc__ = fn.__doc__
        wrapper.counter = self.counter
        return wrapper


class TestAssertReturnValue(object):

    @AssertReturnValue("int(x)>12", "countPassed", "countFailed")
    def _assertReturnValue(self, value):
        return value
     
    def testAssertCounter(self):
        """ 
        verifies the assertion counters
        """
        self._assertReturnValue(24)
        assert self._assertReturnValue.counter['countPassed'] == 1
        assert self._assertReturnValue.counter['countFailed'] == 0

        self._assertReturnValue(-2)
        assert self._assertReturnValue.counter['countPassed'] == 1
        assert self._assertReturnValue.counter['countFailed'] == 1


