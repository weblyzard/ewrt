#!/usr/bin/env python

# (C)opyrights 2008-2009 by Heinz-Peter Lang <heinz@langatium.net>
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


__version__ = "$Header$"

import logging, unittest
from eWRT.util.exception import SNMPException

def sendSNMPTrap(message, module, level):
    '''
    sends a SNMP message
    @param message: String that should be sent
    @param level: SNMP levels ('ok', 'warning', 'critical', 'unknown') 
    '''
    try:
        raise SNMPException(module, message, level=level)
    except SNMPException:
        print 'Sent a SNMP "%s": "%s"' % (level, message)


class SNMPHandler(logging.Handler):
    ''' Logging handler for sending SNMP traps'''

    def __init__(self, moduleName):
        ''' constructor calls the logging handler'''
        logging.Handler.__init__(self)
        self.moduleName = moduleName
    
    def emit(self, record):
        ''' sends the message '''
        level = record.levelname
        if level == 'CRITICAL' or level == 'ERROR':
            level = 'critical'
        elif level == 'WARNING':
            level = 'warning'
        elif level == 'DEBUG' or level == 'INFO':
            level = 'ok'
        else:
            level = 'unknown'
        
        sendSNMPTrap(record.msg, self.moduleName, level)

class TestHandler( unittest.TestCase ):
    
    def testHandler(self):
        ''' tests the handler '''
        
        # Testing the snmp logging
        logger = logging.getLogger('snmp')
        snmpHandler = SNMPHandler('webLyzard.test')
        snmpHandler.setLevel(logging.ERROR)
        logger.addHandler(snmpHandler)
        
        logging.debug('debug')
        logging.info('info')
        logging.warning('warning')
        logging.error('error')
        logging.critical('critical')
    
        
if __name__ == '__main__':
    
    unittest.main()
