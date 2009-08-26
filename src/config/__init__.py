#!/usr/bin/env python

""" @package eWRT.config
    evaluates ~/.eWRTrc and publishes the values"""

# (C)opyrights 2004-2009 by Albert Weichselbraun <albert@weichselbraun.net>
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



__Revision__="$Header$"

import sys
from os.path import expanduser
from warnings import warn
sys.path.append( expanduser("~/.eWRT/") )

try:
    from siteconfig import *
except ImportError:
    warn("Could not finde siteconfig.py in ~/.eWRT")


# $Id$
