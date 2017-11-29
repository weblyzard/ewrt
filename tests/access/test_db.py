#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from nose.plugins.attrib import attr

from eWRT.access.db import PostgresqlDb


class TestDB(unittest.TestCase):
    """ @class TestDB
        db test cases 
    """
    @attr("db")
    def test_context_protocol(self):
        """ tests the db module's support for the context protocoll """
        from eWRT.config import DATABASE_CONNECTION
        with PostgresqlDb( **DATABASE_CONNECTION['wikipedia'] ) as q:
            assert len( q.query("SELECT * FROM concept LIMIT 5")) == 5

    @attr("db")
    def test_multi_processing(self):
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
    