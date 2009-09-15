#!/usr/bin/env python
"""
 @package eWRT.ws.geonames
"""

# (C)opyrights 2009 by Albert Weichselbraun <albert@weichselbraun.net>
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


import sys
from eWRT.access.db import PostgresqlDb
from eWRT.util.cache import DiskCached
from eWRT.config import DATABASE_CONNECTION
from eWRT.access.http import Retrieve

class GeoNames(object):
    """ retrieves information for GeoNames ids
        please use the helper classes in utils.georesolve
        to translate geoURLs into geoIDs 
    """

    NEIGHBOURS_SERVICE_URL = "http://ws.geonames.org/neighboursJSON?geonameId=%d" 

    @staticmethod
    @DiskCached("./.geonames-neighbours")
    def getNeighbours(country_id):
        """ returns all neighbours for the given geo id
            (currently only implemented on a country level)
            @param[in] country_id 
            @returns a list containing the neighbours of the given country """

        url = GeoNames.NEIGHBOURS_SERVICE_URL % country_id 
        print url
        jsonData = eval( Retrieve('eWRT.ws.geonames').open(url).read() )
        print jsonData
        return [ e['geonameId'] for e in jsonData['geonames'] ]


class TestGeoNames(object):

    def testGetNeighbours(self):
        assert GeoNames.getNeighbours(2658434) == [2782113, 3017382, 2921044, 3175395, 3042058]
