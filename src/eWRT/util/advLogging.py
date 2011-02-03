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

import logging
from eWRT.util.exception import SNMPException

eWRTlogger = logging.getLogger('eWRT')
fileHandler = logging.FileHandler('/tmp/eWRT.log')
fileHandler.setLevel(logging.DEBUG)
eWRTlogger.addHandler(fileHandler)

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
        if level == 'CRITICAL':
            level = 'critical'
            eWRTlogger.critical(record.msg)
        elif level == 'ERROR':
            level = 'critical'
            eWRTlogger.error(record.msg)
        elif level == 'WARNING':
            level = 'warning'
            eWRTlogger.warning(record.msg)
        elif level == 'INFO':
            level = 'ok'
            eWRTlogger.info(record.msg)
        elif level == 'DEBUG':
            level = 'ok'
            eWRTlogger.debug(record.msg)
        else:
            level = 'unknown'
        
        sendSNMPTrap(record.msg, self.moduleName, level)
        
if __name__ == '__main__':
    
    # Testing the snmp logging
    logger = logging.getLogger('snmp')
    snmpHandler = SNMPHandler('webLyzard.test')
    snmpHandler.setLevel(logging.ERROR)
    logger.addHandler(snmpHandler)
    
    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('error')
    logger.critical('critical')
    