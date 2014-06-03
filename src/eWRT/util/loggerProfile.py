#!/usr/bin/env python

# (C)opyrights 2008-2014 by Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
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
Pre-defined logging profiles
'''


import logging, unittest


DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


def get_stdout_logger(name, level=logging.DEBUG):
    '''
    Returns a logger which reports to standard output
    '''
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(DEFAULT_LOG_FORMAT)

    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    return logger


class TestLogger(unittest.TestCase):
    
    def test_stdout_logger(self):
        ''' tests the logger '''
        
        logger = get_stdout_logger(__file__)
        logger.debug('debug')
        logger.info('info')
        logger.warning('warning')
        logger.error('error')
        logger.critical('critical')
    
        
if __name__ == '__main__':
    unittest.main()
