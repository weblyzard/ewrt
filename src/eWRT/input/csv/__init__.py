#!/usr/bin/env python

'''
::package eWRT.input.csv
Provides support for reading and filtering data from
CSV files based on eval expressions.

::author: Albert Weichselbraun <albert@weichselbraun.net>
'''

from csv import DictReader

# these methods will be available for third party
# modules
from numpy import var, mean


def get_csv_data(csv_file, column_expression_list, filter_expression):
    '''
    ::param csv_file: the file handle of the csv file to process
    ::param column_expression: an eval expression to extract
                               the column data.
                               e.g. ("row['correct']", "row['sv']", )
                                    "max(row['sv'], row['sentiment'])"
    ::filter_expression: a filter expressions that get's
                   evaluate using eval.
                   e.g. "row['correct'] == 'True' and
                         row['sv'] > 0."
    '''
    return [[eval(column_expression) for column_expression
             in column_expression_list]
             for row in DictReader(csv_file) if eval(filter_expression)]
