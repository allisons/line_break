from __future__ import division
import pandas as pd
from pandas import DataFrame, Series
from glob import glob
from string import punctuation as punct

from crf_formatter import features

import sys

TESTDATA = glob(sys.argv[1])
"""
This file takes a raw text file (no expected NLs) and puts it in the
table format appropriate for crf_test for testing.  It outputs to a file
titled "feature_format_" + the file name provided to it
 """


for file in TESTDATA:
    with open(file, "rb") as f:
        text = f.read()
    char_list = list()
    for char in text:
        char_list.append(char)
    feature_matrix = features(char_list, gold_standard=False)
    
    output = "feature_format_" + file[:-4]
    feature_matrix.to_csv(output, encoding='utf-8', sep="\t", header=False, index=False)