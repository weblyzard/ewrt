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
from os import remove


DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


def get_stdout_logger(name, level=logging.DEBUG):
    '''
    Returns a logger which reports to standard output
    ::param name:
        the logger's name
    '''
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(DEFAULT_LOG_FORMAT)

    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    return logger


def get_file_logger(name, filename, level=logging.DEBUG):
    '''
    Returns a logger which logs to the given filename
    ::param name:
        the logger's name
    ::param filename:
        the name of the logfile
    '''
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(DEFAULT_LOG_FORMAT)

    ch = logging.FileHandler(filename)
    ch.setLevel(level)
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    return logger


class TestLogger(unittest.TestCase):

    LOG_FNAME = 'test.log'

    def test_stdout_logger(self):
        ''' tests the logger '''
        
        logger = get_stdout_logger(__file__)
        logger.debug('debug')
        logger.info('info')
        logger.warning('warning')
        logger.error('error')
        logger.critical('critical')

    def test_file_logger(self):
        ''' tests the file logger '''
        logger = get_file_logger(__file__ + "2", self.LOG_FNAME)
        logger.error('test-message')

        with open(self.LOG_FNAME) as f:
            content = str(f.read())
            assert 'test-message' in content
    
        remove(self.LOG_FNAME)

        
if __name__ == '__main__':
    unittest.main()
