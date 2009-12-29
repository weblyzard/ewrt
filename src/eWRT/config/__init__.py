#!/usr/bin/env python

""" @package eWRT.config
    evaluates ~/.eWRT/siteconfig.py and publishes the values"""

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

CMD_HTML_CONV="/usr/bin/lynx -stdin -width=20000 -force_html -nocolor -dump -nolist -nobold -pseudo_inlines=0 -assume_charset=%s -display_charset=utf8"

# --------------------------------------------------------------------------
#
#  Import config variables from locatl siteconfig
#
# --------------------------------------------------------------------------
try:
    sys.path.append( expanduser("~/.eWRT/") )
    from siteconfig import *
except ImportError:
    from warnings import warn
    warn("Could not finde siteconfig.py in ~/.eWRT")
    
    
# $Id$
