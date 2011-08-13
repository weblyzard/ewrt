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

    def __init__(self, evalExpression, counterNameTrue, counterNameFalse):
        self.evalExpression = evalExpression
        self.counterNameTrue = counterNameTrue
        self.counterNameFalse = counterNameFalse

    def assertReturnValue(self, x):
        x = f(*args, **kwargs)
        assert eval(condition)
        return x


class DecoTraceWithArgs(object):
    '''decorator class with ARGUMENTS

       This can be used for unbounded functions and methods.  If this wraps a
       class instance, then extract it and pass to the wrapped method as the
       first arg.
    '''
    
    def __init__(self, *dec_args, **dec_kw):
        '''The decorator arguments are passed here.  Save them for runtime.'''
        self.dec_args = dec_args
        self.dec_kw = dec_kw

        self.label = dec_kw.get('label', 'T')
        self.fid = dec_kw.get('stream', stderr)

    def _showargs(self, *fargs, **kw):

        print >> self.fid, \
              '%s: enter %s with args=%s, kw=%s' % (self.label, self.f.__name__, str(fargs), str(kw))
        print >> self.fid, \
              '%s:   passing decorator args=%s, kw=%s' % (self.label, str(self.dec_args), str(self.dec_kw))

    def _aftercall(self, status):
        print >> self.fid, '%s: exit %s with status=%s' % (self.label, self.f.__name__, str(status))
    def _showinstance(self, instance):
        print >> self.fid, '%s: instance=%s' % (self.label, instance)
        
    def __call__(self, f):
        def wrapper(*fargs, **kw):
            '''
              Combine decorator arguments and function arguments and pass to wrapped
              class instance-aware function/method.

              Note: the first argument cannot be "self" because we get a parse error
              "takes at least 1 argument" unless the instance is actually included in
              the argument list, which is redundant.  If this wraps a class instance,
              the "self" will be the first argument.
            '''

            self._showargs(*fargs, **kw)

            # merge decorator keywords into the kw argument list
            kw.update(self.dec_kw)

            # Does this wrap a class instance?
            if fargs and getattr(fargs[0], '__class__', None):

                # pull out the instance and combine function and
                # decorator args
                instance, fargs = fargs[0], fargs[1:]+self.dec_args
                self._showinstance(instance)

                # call the method
                ret=f(instance, *fargs, **kw)
            else:
                # just send in the give args and kw
                ret=f(*(fargs + self.dec_args), **kw)

            self._aftercall(ret)
            return ret

        # Save wrapped function reference
        self.f = f
        wrapper.__name__ = f.__name__
        wrapper.__dict__.update(f.__dict__)
        wrapper.__doc__ = f.__doc__
        return wrapper


class TimedTest(TestCase):

    @assertReturnValue("int(x)>12", "countPassed", "countFailed")
    def testAssertReturnValue(object):
         return 24
