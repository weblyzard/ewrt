#!/usr/bin/env python

'''
::package eWRT.input.csv
Provides support for reading and filtering data from
CSV files based on eval expressions.

::author: Albert Weichselbraun <albert@weichselbraun.net>
'''

from csv import DictReader


def get_csv_data(fname, column_expression_list, filter_expression):
    '''
    ::param fname: the file to open
    ::param column_expression: an eval expression to extract
                               the column data.
                               e.g. ("row['correct']", "row['sv']", )
                                    "max(row['sv'], row['sentiment'])"
    ::filter_expression: a filter expressions that get's
                   evaluate using eval.
                   e.g. "row['correct'] == 'True' and
                         row['sv'] > 0."
    '''
    with open(fname) as csvfile:
        return [[eval(column_expression) for column_expression
                in column_expression_list]
                for row in DictReader(csvfile) if eval(filter_expression)]
