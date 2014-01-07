#!/usr/bin/env python

""" @package eWRT.util.profile
    google like profiling :)

    @warning
    this library is still a draft and might change considerable
    
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

from StringIO import StringIO
import cProfile, pstats

def profile(fn, logfile="profile.awi"):
    """ profile function """
    prof = cProfile.Profile()
    
    import __main__
    if __main__.__file__.endswith("nosetests"):
        prof = prof.runctx("%s()" % fn.__name__, globals(), locals())
    else:
        prof = prof.runctx("%s()" % fn.__name__, __main__.__dict__, __main__.__dict__ )

    stream = StringIO()
    stats = pstats.Stats(prof, stream=stream)
    stats.sort_stats("time")  # Or cumulative
    stats.print_stats(80)  # 80 = how many to print
    # The rest is optional.
    stats.print_callees()
    stats.print_callers()
    open(logfile,"w").write( stream.getvalue() )

def __testFunction():
    for a in xrange(1000):
        for b in range(1000):
            c = a * b
           
    return c

def testProfile():
    profile(__testFunction)

