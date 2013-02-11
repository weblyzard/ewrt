'''
Convenient methods for file access

@package eWRT.access.file
Created on Dec 6, 2012

@author: albert
'''

from bz2 import BZ2File
from gzip import GzipFile
from os import remove

class File(object):
    """ An intelligent file object that transparently opens compressed
        files.
    """
    
    def __init__(self, fname, mode="r"):
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
        

class TestFile(object):
    
    TESTSTRING = "this is a test"
    
    def test_formats(self):
        for extension in ('.bz2', '.gz', ''):
            self._test_read_write(extension)
    
    @classmethod
    def _test_read_write(cls, extension=""):
        fname = ".testfile"+extension
        
        with open(fname, "w") as f:
            f.write(cls.TESTSTRING)
        
        with open(fname) as f:
            assert f.read() == cls.TESTSTRING
        
        remove(fname)
    