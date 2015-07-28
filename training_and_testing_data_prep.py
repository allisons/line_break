#!/usr/local/bin/python
from __future__ import division
import pandas as pd
from pandas import DataFrame, Series
from lxml import etree
import re
import time
import random 
from string import punctuation as punct
import os.path
from glob import glob
import sys

from crf_formatter import *

#Character based features?
char = False

feat_functs = {"case": case_features, "num": num_features, "punct": punct_features, "casenum": case_num_features, 
"casepunct": case_punct_features, "numpunct": num_punct_features, "allword": word_features}

start = time.time()
sep = "\t"
test_portion = .1
rnd = random.Random()
#rnd.seed(12)

def test_train_fold(paths):
    paths = paths+"/*"
    paths = glob(paths)
    N = len(paths)
    n = int(N*test_portion)
    shuffled = rnd.sample(paths, N)
    testdata = shuffled[:n]
    traindata = shuffled[n:]
    return testdata, traindata 
    
def xml_strip(text):
    old = text
    report_tag = re.compile("<report_text>")
    end_tag = re.compile("</report_text")
    begin = report_tag.search(text)
    end = end_tag.search(text)
    s = begin.start()+13
    e = end.start()
    fixed = text[s:e]
    assert not old == fixed
    return fixed
    
#TESTDATA, TRAINDATA = test_train_fold(sys.argv[1])
TRAINDATA = glob(sys.argv[1]+"/*")
TESTDATA = glob(sys.argv[2]+"/*")
if len(sys.argv) > 3:
    word_features = feat_functs[sys.argv[3]]
else:
    word_features = feat_functs["allword"]


def prepare_train_data(TRAINDATA):
    print "Beginning training data preparation"
    total_features = DataFrame()
    doc_list = list()
    begin_train = time.time()
    for path in TRAINDATA:
        
        with open(path) as f:
            string = f.read()

        if path[-4:] == "xml":
            text = xml_strip(string)
            assert len(text) < len(string)
        else:
            text = string
        feature_matrix=word_features(text)
        
        doc_list.append(feature_matrix)
        total_features = pd.concat([total_features, feature_matrix], axis=0)

    end_train = time.time() - begin_train
    print "Done prepping training data in ", end_train, "seconds"
    end_train = time.time()
    total_features.to_csv('train_features', encoding='utf-8', sep=sep, header=False, index=False)
    save_train = time.time() - end_train
    print "Training features saved"

def prepare_test_data(TESTDATA):
    print "Beginning test data prep"
    begin_test = time.time()
    name = re.compile("/")
    for path in TESTDATA:
        
        with open(path) as f:
            string = f.read()
        if path[-4:] == ".xml":
            text = xml_strip(string)
            assert len(text) < len(string)
        else:
            text = string
        
        feature_matrix = word_features(text)
        idx = name.search(path).start()
        if not os.path.exists("formatted_test_data/"):
            os.mkdir("formatted_test_data")
        filename = "formatted_test_data/feature_format_"+ path[idx+1:-4]
        feature_matrix.to_csv(filename, encoding='utf-8', sep=sep, header=False, index=False)
    end_test = time.time() - begin_test
    print "Test data file prep completed in ", end_test, "seconds"

