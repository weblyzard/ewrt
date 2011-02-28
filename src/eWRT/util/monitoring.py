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

'''
The class NSCA-Service helps the enables to send test-results over the
NSCA service to Nagios. This is a more reliable way of sending messages
directly from programs than with SNMP. On the one hand because they are
not only associated to single service, but also as the configuration is
easier

== Configuration ==

* Install the package nsca 

 aptitude install nsca 

* On the monitoring system:

** edit the file ''/etc/nsca.cfg'': 
** set a password and an appropriate encryption method

* On the host:

** edit the file ''/etc/send_nsca.cfg''
** enter the above password and encryption method

== Configuring eWRT == 

'''

import os, subprocess, commands, socket, logging
from string import Template

SEND_NSCA_PATH = os.path.join(os.sep, 'usr', 'sbin', 'send_nsca')
SEND_NSCA_CONFIG = os.path.join(os.sep, 'etc' ,'send_nsca.cfg')
MONITORING_SERVER = '\'localhost\''

logger = logging.getLogger('eWRT')

class NSCA( object ):
    ''' class NSCA Service helps sending test results to Nagios '''
    
    @staticmethod
    def send(message, status, service_name, src_host=None):
        ''' sends the '''
    
        if src_host == None:
    
            src_host = socket.gethostname()
#            TODO think about setting it to localhost instead
#            src_host = 'localhost'
    
        STATUS = [0, 1, 2, 3]
    
        assert status in STATUS
                
        formattedResult = '{src_host};{service_name};{status};{message}'.format(src_host=src_host, service_name=service_name, status=status, message=message)
        cmd = [SEND_NSCA_PATH, '-H',  MONITORING_SERVER, '-d', '\';\'', '-c', SEND_NSCA_CONFIG]

        out = commands.getstatusoutput("echo '%s' | %s " % (message, ' '.join(cmd)))

        if not out[1] == '1 data packet(s) sent to host successfully.':
            logger.error('Could not send the data packet!')
    
       
if  __name__ == '__main__':
    
    NSCA.send('Ahoi', 0, 'TEST')