#!/usr/bin/env python
"""
 @package eWRT.ws.geonames.gazetteer.exception
 exceptions related to the gazetteer class

"""

# (C)opyrights 2009 by Heinz Lang <heinz.lang@wu.ac.at>
#                      Albert Weichselbraun <albert@weichselbraun.net>
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


class GazetteerEntryNotFound(Exception):
    """ @class GazetteerEntryNotFound
        Base class for gazetteer lookup errors 
    """
    def __init__(self, id, query):
        self.id = id
        self.query = query
        print id, query

    def __str__(self):
        return "Gazetteer lookup for entity-id '%s' failed." % (self.id)


class GazetteerNameNotFound(Exception):
    """ @class GazetteerNameNotFound
        This exception is thrown if a lookup name has not been found in the gazetteer
    """

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Gazetteer lookup of name '%s' failed." % (self.name)

