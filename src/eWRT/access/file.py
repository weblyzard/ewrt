'''
Convenient methods for file access

@package eWRT.access.file
Created on Dec 6, 2012

@author: albert
'''

from bz2 import BZ2File
from gzip import GzipFile
from os import remove

class CompressedFile(object):
    ''' An intelligent file object that transparently opens compressed
        files.
    '''
    COMPRESSION_EXT = ('bz2', 'gz')
    
    def __init__(self, fname, mode='r'):
        self.name = fname
        if fname.endswith(".gz"):
            self.fhandle = GzipFile(fname, mode)
        elif fname.endswith(".bz2"):
            self.fhandle = BZ2File(fname, mode)
        else:
            self.fhandle = open(fname, mode)

    def __enter__(self):
        return self.fhandle

    
    def __exit__(self, e_type, e_value, e_traceback):
        self.fhandle.close()


    @classmethod
    def open(cls, fname, mode='r'):
        return CompressedFile(fname, mode).fhandle


    @classmethod
    def get_extension_list(cls, fname):
        '''
        @return: a list of file extensions of this file
                 ignoring extensions indicating file compression.

        e.g. 'test.awp.csv.bz2' -> ['csv', 'awp']
        '''
        ext_list = fname.split(".")
        ext_list.reverse()
                                
        return ext_list if ext_list[0] not in cls.COMPRESSION_EXT else ext_list[1:]


class TestFile(object):
    
    TESTSTRING = "this is a test"
    
    def test_formats(self):
        for extension in ('.bz2', '.gz', ''):
            self._test_read_write(extension)
    
    @classmethod
    def _test_read_write(cls, extension=""):
        fname = ".testfile.txt"+extension
        
        with CompressedFile(fname, "w") as f:
            f.write(cls.TESTSTRING)
        
        with CompressedFile(fname) as f:
            assert f.read() == cls.TESTSTRING
            assert CompressedFile.get_extension_list(fname)[0] == 'txt'
        
        remove(fname)
    
