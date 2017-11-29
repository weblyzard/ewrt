#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from eWRT.util.assert_return import AssertReturnValue


class TestAssertReturnValue(unittest.TestCase):

    @AssertReturnValue("int(x)>12", "countPassed", "countFailed")
    def _assertReturnValue(self, value):
        return value
     
    def testAssertCounter(self):
        """ 
        verifies the assertion counters
        """
        self._assertReturnValue(24)
        assert self._assertReturnValue.counter['countPassed'] == 1
        assert self._assertReturnValue.counter['countFailed'] == 0

        self._assertReturnValue(-2)
        assert self._assertReturnValue.counter['countPassed'] == 1
        assert self._assertReturnValue.counter['countFailed'] == 1
        
if __name__ == '__main__':
    unittest.main()