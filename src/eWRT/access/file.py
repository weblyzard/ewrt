'''
Convenient methods for file access

@package eWRT.access.file
Created on Dec 6, 2012

@author: albert
'''

from bz2 import BZ2File
from gzip import GzipFile
from os.path import basename


class CompressedFile(object):
    ''' An intelligent file object that transparently opens compressed
        files.
    '''
    COMPRESSION_EXT = ('bz2', 'gz')

    def __init__(self, fname, mode='rb'):  # ported to python3 (SV)
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
    def open(cls, fname, mode='rb'):  # ported to python3 (SV)
        return CompressedFile(fname, mode).fhandle

    @classmethod
    def get_extension_list(cls, fname):
        '''
        :param fname: the file name to analyze
        :rtype: a list of file extensions of this file
                ignoring extensions indicating file compression.

        e.g. 'x/y/test.awp.csv.bz2' -> ['csv', 'awp']
        '''
        ext_list = basename(fname).split(".")
        ext_list.reverse()
        return ext_list if ext_list[0] not in cls.COMPRESSION_EXT \
            else ext_list[1:]
