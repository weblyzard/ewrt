#!/usr/bin/env python

from eWRT.input.csv import get_csv_data
from eWRT.util.module_path import get_resource

TEST_FILE = get_resource(__file__, ('test.csv', ))

def test_csv_data():
    CORRECT = (2,4,6)
    for correct, computed in zip(CORRECT, get_csv_data(TEST_FILE,
                                                       'int(row["a"])+int(row["b"])',
                                                       'row["show"]=="True"')):
        assert correct == computed
