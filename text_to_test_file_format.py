from __future__ import division
import pandas as pd
from pandas import DataFrame, Series
from glob import glob
from string import punctuation as punct

from crf_formatter import *

import sys

TESTDATA = glob(sys.argv[1])
testfolder = "formatted_test_data/"
if not os.path.exists("formatted_test_data/"):
    os.mkdir("formatted_test_data")

feat_functs = {"case": case_features, "num": num_features, "punct": punct_features, "casenum": case_num_features, 
"casepunct": case_punct_features, "numpunct": num_punct_features, "allword": word_features}

"""
This file takes a raw text file (no expected NLs) and puts it in the
table format appropriate for crf_test for testing.  It outputs to a file
titled "feature_format_" + the file name provided to it
 """

if len(sys.argv) > 2:
    word_features = feat_functs[sys.argv[2]]
else:
    word_features = feat_functs["allword"]

for file in TESTDATA:
    with open(file, "rb") as f:
        text = f.read()
    feature_matrix=word_features(text, gold_standard=False)
    
    output = "formatted_test_data/feature_format_" + file[:-4]
    feature_matrix.to_csv(output, encoding='utf-8', sep="\t", header=False, index=False)