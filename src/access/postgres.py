#!/usr/bin/env python
"""
 provides an interface for access to a postgresql database 
"""

# (C)opyrights 2008 by Albert Weichselbraun <albert@weichselbraun.net>
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



__revision__ = "$Revision$"

import pg
from types import StringTypes

DBNAME   = "amazon"

class DB:
    """ provides generall database access """
   
    def __init__(self, dbname=DBNAME):
    	""" inits the database class """
	self.dbname   = dbname


    def query(self,qu):
    	""" processes a queries to the postgresql database and returns
            the result."""
	db=pg.connect(self.dbname)
	if type(qu) in StringTypes: qu=(qu,)
	for q in qu:
		try:
			tmp=db.query(q)
		except:
			continue

        db.close()
	try:
		return tmp.dictresult()
	except:
		return None


