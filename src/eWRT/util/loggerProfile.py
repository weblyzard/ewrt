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
import os
import logging
import unittest

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

LOG_LEVELS = {'CRITICAL': logging.CRITICAL,
              'ERROR': logging.ERROR,
              'WARNING': logging.WARNING,
              'INFO': logging.INFO,
              'DEBUG': logging.DEBUG}
LOG_FORMAT = {'standard': '%(asctime)s %(levelname)s %(pathname)s:%(lineno)d.%(funcName)s()  %(message)s',
              'compact': '%(levelname)s %(message)s'}
EWRT_LOG_LVL = 65
DEFAULT_LOG_LEVEL = 'ERROR'
DEFAULT_LOG_FILE = '/tmp/eWRT.log'

def init_logging(log_file=DEFAULT_LOG_FILE, log_level=None, 
                 max_bytes=102400, max_files=5, log_format=None):
    ''' inits the logger, if default log file is used, a rotating file-handler 
    will be added to the logger, otherwise it adds a standard FileHandler. In 
    addition to that it also streams the streams the result to stdout.
    :param log_file: log file to use
    :param log_level: log level
    :param max_bytes: maximum bytes for the RotatingFileHandler
    :param max_files: maximum number of files for the RotatingFileHandler
    :param log_format: standard or compact
    :returns: the initialized worker. 
     ''' 
    from logging import FileHandler
    from logging.handlers import RotatingFileHandler
    logger = logging.getLogger('')
    logging.addLevelName(65, 'EWRT_INFO')
     
    if not log_format or log_format not in LOG_FORMAT:
        log_format = 'standard'
    
    if len(logger.handlers):
        logger.handlers = []
    
    if log_level and isinstance(log_level, basestring):
        log_level = log_level.upper()
        if log_level in LOG_LEVELS:
            log_level = LOG_LEVELS[log_level]
        else: 
            print 'log_level %s not found using "ERROR"' % log_level
            
    if not log_level: 
        log_level = DEFAULT_LOG_LEVEL
    
    hdlr = logging.StreamHandler()

    logger.addHandler(hdlr)
    hdlr.setLevel(log_level)
    logger.setLevel(log_level)
    formatter = logging.Formatter(LOG_FORMAT.get(log_format))
    hdlr.setFormatter(formatter)
   
    # setting loglevel of tldextract to ERROR to prevent extensive messages
    tld_logger = logging.getLogger('tldextract')
    tld_logger.setLevel(logging.ERROR)
    
    try:
        file_hdlr = None
        
        if log_file: 
            if log_file == DEFAULT_LOG_FILE:
                file_hdlr = RotatingFileHandler(log_file, 
                                                maxBytes=max_bytes,
                                                backupCount=max_files, 
                                                encoding='utf-8')
            else: 
                log_dir = os.path.dirname(log_file) 
                
                if not os.path.exists(log_dir):
                    os.makedirs(log_dir)
                
                file_hdlr = FileHandler(filename=log_file, 
                                        encoding='utf-8')
         
        if file_hdlr:
            file_hdlr.setLevel(log_level)
            file_hdlr.setFormatter(formatter)
            logger.addHandler(file_hdlr)
            
    except Exception, e: 
        logger.error('Couldnt create LogHandler %s: %s' % (log_file, e))
        
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
    
        os.remove(self.LOG_FNAME)

        
if __name__ == '__main__':
    unittest.main()
