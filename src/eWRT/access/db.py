#!/usr/bin/env python
"""
 @package eWRT.access.db
 interfaces for access classes
"""

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


__author__   = "Albert Weichselbraun"
__revision__ = "$Revision$"


from types import StringTypes
from warnings import warn
try:
    import psycopg2 
    import psycopg2.extras
except ImportError:
    warn("Cannot import postgresql library.")
try:
    import MySQLdb
except ImportError:
    warn("Cannot import mysql library.")



class IDB(object):
    """ @interface
        database access interface
     """

    def connect(self):
        """ connects to the database """   

    def query(self,qu):
        """ processes a queries to the database and returns
            the result.
            @param[in] query (list or string)
            @returns the result as dictionary
        """
        raise NotImplementedError

    def close(self):
        """ closes the database connection """
        raise NotImplementedError


class MysqlDb(IDB):

        def __init__(self, dbname, host="", username="", passwd=""):
                self.dbname   = dbname
                self.host     = host
                self.username = username
                self.passwd   = passwd
                self.connect()

        def connect(self):
                self.db=MySQLdb.connect(host=self.host, user=self.username, passwd=self.passwd, db=self.dbname)


        def query(self,query):
                """ queries the database and stores the result in a dict """
                crs=self.db.cursor(MySQLdb.cursors.DictCursor)

                if type(query) in StringTypes: query=(query,)
                for q in query:
                    crs.execute(q)
                tmp=crs.fetchall()
                crs.close()
                return tmp


        def close(self):
                self.db.close()


class PostgresqlDb(IDB):
    """ @class 
        provides generall database access """

    DEBUG = False

    def __init__(self, dbname, host="", username="", passwd=""):
        """ inits the database class """
        self.dbname   = dbname
        self.host     = host
        self.username = username
        self.passwd   = passwd
        self.connect()

    def connect(self):
        self.db=psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (self.dbname, self.username, self.host, self.passwd))

    def query(self,qu):
        """ queries the postgresql database """
        if type(qu) in StringTypes: qu=(qu,)
        if PostgresqlDb.DEBUG: 
            print qu
        cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        [ cur.execute(q) for q in qu ]
        return cur.fetchall()


    def close(self):
        self.db.close()
