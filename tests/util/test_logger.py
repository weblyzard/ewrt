#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import logging

from os import remove

from eWRT.util.loggerProfile import get_file_logger, get_stdout_logger
from eWRT.util.advLogging import SNMPHandler


class TestHandler( unittest.TestCase ):
    
    def test_handler(self):
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
