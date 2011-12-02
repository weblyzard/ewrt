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

'''

import os, subprocess, commands, socket, logging
from string import Template

SEND_NSCA_PATH = os.path.join(os.sep, 'usr', 'sbin', 'send_nsca')
SEND_NSCA_CONFIG = os.path.join(os.sep, 'etc' , 'send_nsca.cfg')
MONITORING_SERVER = '\'tor.wu.ac.at\''

class NSCA(object):
    ''' class NSCA Service helps sending test results to Nagios '''

    @staticmethod
    ## sends a NSCA message to the monitoring server
    # @param status: service status (0->OK, 1->warning, 2->critical, 3->unknown)
    # @param service_name: name of the service 
    # @param src_host: name of the host the server is running on. by default the 
    #                  script will run socket.gethostname()
    # @param performance:     
    def send(message, status, service_name, src_host=None, performance=[],
             monitoringServer=MONITORING_SERVER):
        ''' sends the '''

        if src_host == None:

            src_host = socket.gethostname()

        STATUS = [0, 1, 2, 3]

        assert status in STATUS

        message = '{src_host};{service_name};{status};{message}'.format(src_host=src_host, service_name=service_name, status=status, message=message)

        if len(performance) > 0 :
            message = '%s | %s ' % (message, ' '.join([p.message for p in performance]))

        cmd = [SEND_NSCA_PATH, '-H', monitoringServer, '-d', '\';\'', '-c', SEND_NSCA_CONFIG]
        print "echo '%s' | %s " % (message, ' '.join(cmd))
        out = commands.getstatusoutput("echo '%s' | %s " % (message, ' '.join(cmd)))

        if not out[1] == '1 data packet(s) sent to host successfully.':
            print 'Could not send the data packet:', out[1]
        else:
            print out[1]


## Performance allows to add performance information to a NSCA message 
class Performance(object):

    ## constructor of Performance
    # @param label: name of the 'variable', e.g. time
    # @param value: value of the 'variable', e.g. 0.654
    # @param unit: unit of the value, good values are:
    #                   ... integer value
    #                 s ... seconds
    #                 % ... percentage
    #                 B, KB, MB, TB ... byte, kilo-, mega', terabyte
    #                 c ... counter
    # @param warn: threshold for warning status
    # @param critical: threshold for critical status
    # @param min: minimum value
    # @param max: maximum value  
    def __init__(self, label, value, unit='', warn='', critical='', min='', max=''):

        label = '\'%s\'' % label
        assert isinstance(value, (int, long, float, complex))
        assert unit in ('', 's', '%', 'B', 'KB', 'MB', 'TB', 'c')

        self.message = '%s=%s%s;%s;%s;%s;%s' % (label, value, unit, warn, critical, min, max)
        print self.message

if  __name__ == '__main__':

    NSCA.send('just a test!', 0, 'webLyzard notifications', 'tor.wu.ac.at', [Performance('test', 3, 's')])
