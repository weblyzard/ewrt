#!/usr/bin/env python

"""
@package: eWRT.input.stock
Provides access to historical stock market data

Interesting indices to support in the future:
* BALTIC DRY INDEX (BDIY:IND)
* Howe Robinson Container Index
"""

from bz2 import BZ2File
from csv import reader
from glob import glob
from os.path import dirname, basename, join as os_join
from collections import namedtuple
from datetime import datetime
from twisted.python.text import strFile

from eWRT.util.module_path import get_resource

extract_index_name = lambda fname: basename(fname).split(".")[0]
DATA_DIR = get_resource(__file__, ('data', ) )

Quote = namedtuple('quote', 'date last open high low change_percentage')


class StockIndex(object):
    SUPPORTED_INDICES = { extract_index_name(fname):fname 
                         for fname in glob(DATA_DIR+"/*.idx.bz2")  }
    SUPPORTED_FUTURES = { extract_index_name(fname):fname 
                          for fname in glob(DATA_DIR+"/*.ftidx.bz2")  }
    DATE_FORMAT = "%b %d, %Y"

    @classmethod
    def get_index(cls, index_name):
        """retrieves data from the given index in csv format
           @param index_name: the name of the index
        """
        return cls._read_index_filen(cls.SUPPORTED_INDICES[index_name])
    
    
    @classmethod
    def get_future(cls, future_name):
        """retrieves data from the given future in csv format
           @param future_name: the name of the future
        """
        print cls.SUPPORTED_FUTURES[future_name]
        return cls._read_index_filen(cls.SUPPORTED_FUTURES[future_name])[1:]
        
        
    @classmethod
    def _read_index_filen(cls, fname):
        """ @return: the contents of the given index file.
        """
        with BZ2File(fname) as f:
            result =[Quote._make(cls._convert_tuple(row)) 
                     for row in reader(f, delimiter="\t") if row] 
            
        return result
    
    
    @classmethod
    def _convert_tuple(cls, t):
        """ converts the string in the given tuple to the respective 
            float/_date datatypes.
            @param t: the input tuple
            @return: output tuple with the correct datatypes 
        """
        #_date _last _open _high _low %_change'
        _date, _last, _open, _high, _low, _change = t
        return (datetime.strptime(_date, cls.DATE_FORMAT), float(_last),
                float(_open), float(_high), float(_low), float(_change[:-1]))
        
    
if __name__ == '__main__':
    s_list = StockIndex.get_index('dax')
    f_list = StockIndex.get_future('dax')
    delta = []
    Analysis = namedtuple('analysis', "delta volatility change_percentage")
    for s,f in zip(s_list,f_list):
        print s.date, f.date
        assert s.date == f.date
        delta.append( (s.date, Analysis(f.last-s.last, s.last-s.open, s.change_percentage)) )
    
    delta.sort(key=lambda x:x[1].delta)
    print delta[:10]
        
