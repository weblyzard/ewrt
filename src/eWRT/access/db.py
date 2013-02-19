#!/usr/bin/env python
"""
@package eWRT.access.db` -- database access
========================================
"""

# (C)opyrights 2004-2010 by Albert Weichselbraun <albert@weichselbraun.net>
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
from nose.plugins.attrib import attr
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

# logging
import logging
log = logging.getLogger(__name__)



class IDB(object):
    """ @interface IDB
        database access interface

        @remarks
        supports the context protocal
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

    def __enter__(self):
        """ support fo the context protocol """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """ context protocol support """
        if exc_type != None:
            log.critical("Database error: %s" % exc_type)
        self.close()
        


class MysqlDb(IDB):

    def __init__(self, dbname, host="", username="", passwd="", connect=True):
        """ @param[in] connect immediately connect to the database
        """
        self.dbname   = dbname
        self.host     = host
        self.username = username
        self.passwd   = passwd

        if connect:
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
    """ @class  PostgresqlDb
        provides generall database access """

    __db = {}           # cache db connections
    DEBUG = False

    def __init__(self, dbname, host="", username="", passwd="", multiThreaded=True, connect=True):
        """ inits the database class 
            @param[in] multiThreaded specifies whether the connection will be used
                                     in a multi-threaded environment.
        """
        self.dbname   = dbname
        self.host     = host
        self.username = username
        self.passwd   = passwd
        self.db       = None
        self.multiThreaded = multiThreaded
        if connect:
            self.connect()

    def connect(self):
        """ connects to the database

            @remarks 
            caches the connection if multiThreaded is False; the connection caching does not
            work in multi-threaded environments
        """
        if self.multiThreaded:
            self.db = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (self.dbname, self.username, self.host, self.passwd)) 

        else:
            dbKey = (self.dbname, self.username, self.host, self.passwd)
            if dbKey not in self.__db:
                self.__db[dbKey] = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (self.dbname, self.username, self.host, self.passwd)) 
            self.db= self.__db[dbKey]


    def query(self,qu):
        """ @param[in] qu a list or string containing the database quer(y|ies)
            @returns the query results
         """
        if type(qu) in StringTypes: qu=(qu,)
        if PostgresqlDb.DEBUG: 
            log.debug( "Query: %s" % qu )
        cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        [ cur.execute(q) for q in qu ]
        return cur.fetchall()
    
    def execute(self, q):
        cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        return cur.execute(q)
    
    def getCursor(self):
        return self.db.cursor()
    
    def commit(self):
        self.db.commit()


    def close(self):
        self.db.close()


class TestDB(object):
    """ @class TestDB
        db test cases 
    """
    @attr("db")
    def testContextProtocol(self):
        """ tests the db module's support for the context protocoll """
        from eWRT.config import DATABASE_CONNECTION
        with PostgresqlDb( **DATABASE_CONNECTION['wikipedia'] ) as q:
            assert len( q.query("SELECT * FROM concept LIMIT 5")) == 5

    @attr("db")
    def testMultiProcessing(self):
        """ tests multiprocessing """
        from multiprocessing import Pool
        p = Pool(4)
        qq = 8 * ["SELECT * FROM concept LIMIT 1"]

        res = p.map(t_multiprocessing, qq)


def t_multiprocessing(q):
    """ @remarks
        helper function for the multi processing test case
    """
    from eWRT.config import DATABASE_CONNECTION

    db = PostgresqlDb( **DATABASE_CONNECTION['wikipedia'] )
    r = db.query( q )
    db.close()
    return r
    
