#!/usr/bin/env python

""" @package eWRT.util.exception """

# (C)opyrights 2008-2010 by Albert Weichselbraun <albert@weichselbraun.net>
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

__author__    = "Albert Weichselbraun"
__revision__  = "$Id$"
__copyright__ = "GPL"

from eWRT.config import *
from subprocess import call


global MODULE 
MODULE = SNMP_MODULE_NAME

class SNMPException(Exception):
    """ reports an exception to snmp """

    def __init__(self, module_name, msg, level="warning"):

        assert module_name in MODULE
        assert level in SNMP_LOG_LEVEL
        assert "\n" not in msg

        self.module_name = module_name
        self.msg         = msg
        self.level       = level
        self._sendSNMPNotification( module_name, msg, level)


    def _sendSNMPNotification(self, module_name, msg, level):
        """
        sends a copy of the exception to the snmp server
        @param[in] module_name ... name of the module throwing the exception
        @param[in] msg         ... the exception message string
        @param[in] level       ... level of the log message (ok, warning, critical)
        """
        cmd = ["snmptrap", "-v", "2c", 
                           "-c", SNMP_HOST_CFG['community_string'],  
                           SNMP_HOST_CFG['server'], "''", 
                           SNMP_HOST_CFG['oid'], 
                           SNMP_MODULE_NAME[module_name], "s", msg,
                           SNMP_MODULE_NAME['webLyzard.log.level'], "i", SNMP_LOG_LEVEL[level] ]
        call(cmd)


    def __str__(self):
        return "Exception in '%s': %s" % (self.module_name, self.msg)


class TestSNMPException(object):
    
    def testSNMPException(self):
        """ tests an SNMP exception """
        try:
            raise SNMPException("webLyzard.experimental", "This is a test exception")
        except SNMPException:
            pass

    def testQuoting(self):
        try:
            raise SNMPException("webLyzard.experimental", "Hallo wie geht's?")
        except SNMPException:
            pass
                           
#t = TestSNMPException()
#t.testSNMPException()
# $Id$
