#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Nov 29, 2017

.. codeauthor: max goebel <mcgoebel@gmail.com>
'''
from builtins import bytes
import unittest

from os import remove

from eWRT.access.file import CompressedFile


class TestFile(unittest.TestCase):

    TESTSTRING = "this is a test"

    def test_formats(self):
        for extension in ('.bz2', '.gz', ''):
            self._test_read_write(extension)

    @classmethod
    def _test_read_write(cls, extension=""):
        fname = ".testfile.txt"+extension

        with CompressedFile(fname, "wb") as f:
            try:  # porting to python3 (SV)
                f.write(bytes(cls.TESTSTRING, 'UTF-8'))  # python3
            except:
                f.write(cls.TESTSTRING)  # python2

        with CompressedFile(fname) as f:
            #assert f.read() == cls.TESTSTRING # python2
            new_string = f.read().decode('UTF-8')  # python3 (SV)
            assert new_string == cls.TESTSTRING
            assert CompressedFile.get_extension_list(fname)[0] == 'txt'

        remove(fname)

if __name__ == '__main__':
    unittest.main()