#!/usr/bin/env python
"""
 @package eWRT.ws.stat.eval.metrics
 Standard IR evaluation metrics such as
  * precision
  * recall
  * F1 measure
"""

# (C)opyrights 2010 by Albert Weichselbraun <albert@weichselbraun.net>
#                   and others (as outlined in the functions.
#
# The code published in this module is either under the GNU General
# Public License (see below) or under the license specified in the 
# function. 
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
#


def precision(relevant, retrieved):
    """ returns the precision of the given sets 
        @param[in]  relevant set of relevant terms
        @param[in] retrieved set of retrieved terms
        @returns the precision
    """
    assert isinstance(relevant, set) 
    assert isinstance(retrieved, set) 

    return float( len(relevant.intersection(retrieved)) ) / len(retrieved)


def recall(relevant, retrieved):
    """ returns the recall of the given sets 
        @param[in]  relevant set of relevant terms
        @param[in] retrieved set of retrieved terms
        @returns the recall
    """
    assert isinstance(relevant, set) 
    assert isinstance(retrieved, set) 

    return float( len(relevant.intersection(retrieved)) ) / len(relevant)


def fMeasure(p, r, beta=1.):
    """ returns the F-measure for the given precision and recall
        @param[in] p precision
        @param[in] r recall 
        @param[in] beta  weight used to compute the f mesure
        @returns the F-Measure
    """
    return (1+beta*beta) * (p*r)/(beta*beta*p+r)


class TestEvaluationMetrics(object):
    """ tests the evaluation metrics """

    a = set( (1,3,8,9) )
    b = set( (1,3,10,12) )
    c = set( (1,3) )
    d = set( (10, 11) )

    def testPrecision(self):
        assert precision(self.a, self.b) == 0.5
        assert precision(self.a, self.a) == 1.0
        assert precision(self.a, self.c) == 1.0
        assert precision(self.a, self.d) == 0.0

    def testRecall(self):
        assert recall(self.a, self.a) == 1.0
        assert recall(self.a, self.b) == 0.5
        assert recall(self.a, self.c) == 0.5
        assert recall(self.a, self.d) == 0.0

    def testFMeasure(self):
        assert fMeasure(1.,1.,1.) == 1
        assert fMeasure(1.,0.,1.) == 0.0
        assert fMeasure(1.,0.5,1.) == 1/1.5


