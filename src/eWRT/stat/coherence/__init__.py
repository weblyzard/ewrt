#!/usr/bin/env python
"""
 @package eWRT.ws.stat.coherence
 Determines how strongly two terms are connected to each other
"""

# (C)opyrights 2010 by Albert Weichselbraun <albert@weichselbraun.net>
#                      Johannes Duong <johannes.duong@wu.ac.at>
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

from eWRT.ws.TagInfoService import TagInfoService
from unittest import TestCase
from eWRT.util.cache import DiskCache

from math import exp

class Coherence(object):
    """ @class Coherence
        abstract class for computing the coherence between 
        terms """

    def __init__(self, dataSource, cache=True):
        """ @param[in] dataSource implementing the TagInfoService Interface """
        assert isinstance(dataSource, TagInfoService) 
        self.dataSource  = dataSource
        if cache==True:
            diskCache       = DiskCache("./.coherence-tagcount-cache", 2)
            self.getTagCount = lambda tt: diskCache.fetchObjectId( self.dataSource.__class__.__name__ + str(tt), 
                                                                   self.dataSource.getTagInfo, tt)
        else:
            self.getTagCount = self.dataSource.getTagInfo

    @staticmethod
    def getCoherence(nx, ny, nt):
        """ @param[in] nx  counts of term1
            @param[in] ny  counts of term2
            @param[in] nt counts of term1 together with term2
            @returns the coherence
        """
        raise NotImplemented

    def getTermCoherence(self, t1, t2):
        """ @param[in] t1 term1
            @param[in] t2 term2
            @returns the coherence between these two terms
        """        
        nx = self.getTagCount( (t1, ) )
        ny = self.getTagCount( (t2, ) )
        nt = self.getTagCount( (t1, t2) )
        return self.getCoherence(nx, ny, nt)


class DiceCoherence(Coherence):
    """ @class DiceCoherence
        computes the dice coherence for the given terms """

    @staticmethod
    def getCoherence(nx, ny, nt):
        """ @param[in] nx  counts of term1
            @param[in] ny  counts of term2
            @param[in] nt counts of term1 together with term2
            @returns the coherence
        """
        try:
            return 2*float(nt)/float(ny+ny)
        except ZeroDivisionError:
            return None

class PMICoherence(Coherence):
    """ @class PMICoherence
        computes the coherence based on the pointwise mutual
        information (PMI)
    """

    @staticmethod
    def getCoherence(nx, ny, nt):
        """ @param[in] nx  counts of term1
            @param[in] ny  counts of term2
            @param[in] nt counts of term1 together with term2
            @returns the coherence
        """
        nx, ny, nt = float(nx), float(ny), float(nt)

        nz = nx + ny + nt
        try:
            fx = (nx/nz)*exp((nx/nz)*-1)
            fy = (ny/nz)*exp((ny/nz)*-1)
            ft = (nt/nz)*exp((nt/nz)*-1)
            return ft/(fx*fy)
        except ZeroDivisionError:
            return None
        


class TestCoherence(TestCase):
    
    def testDice(self):
        """ tests the computation of the dice coefficient 
            based on the example in
              http://en.wikipedia.org/wiki/Dice's_coefficient
        """
        assert DiceCoherence.getCoherence( 4, 4, 1 ) == 0.25

    def testPMI(self):
        """ tests the computation of the PMI based on the results
            from wilson's paper 
        """
        c = PMICoherence.getCoherence
        self.assertAlmostEqual( c(4710000000, 125000, 897), 0.0195069043716 ) # one - coup whole wheat flour
        self.assertAlmostEqual( c(3670000, 870000, 897), 0.00346634415814)    # one coup - whole wheat flour
        self.assertAlmostEqual( c(4270, 2690000, 897), 0.571746307316)        # one coup whole - wheat flour
        self.assertAlmostEqual( c(2320, 33400000.0, 897), 1.05103564089)      # one coup whole wheat - flour
        
    def testPMIZero(self):
        """ tests the handling of PMI values of no counts are found """
        c = PMICoherence.getCoherence
        assert c(0,12,0) == None

