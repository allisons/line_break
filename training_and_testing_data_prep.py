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
import argparse

from crf_formatter import features



start = time.time()
sep = "\t"
test_portion = .1
rnd = random.Random()
rnd.seed(31)

def test_train_fold(paths):
    paths = paths+"/*"
    paths = glob(paths)
    N = len(paths)
    n = int(N*test_portion)
    shuffled = rnd.sample(paths, N)
    testdata = shuffled[:n]
    traindata = shuffled[n:]
    return testdata, traindata 

if 1: #shuffley bits    
    TESTDATA, TRAINDATA = test_train_fold(sys.argv[1])

else:
    TRAINDATA1 = glob('sliter_gold_standard/*')
    TRAINDATA2 = glob('first_50/*')
    TRAINDATA = TRAINDATA1 + TRAINDATA2
    TESTDATA = glob('test_files/*')

if 1: #prepping training data
    print "Beginning training data preparation"
    total_features = DataFrame()
    doc_list = list()
    begin_train = time.time()
    for path in TRAINDATA:
        
        with open(path) as f:
            string = f.read()

        if path[-3:] == "xml":
            root = etree.fromstring(string)
            tree = etree.parse(path)

            #Removes vestigial html tags at end of file.
            tag = re.compile("<start | <START")
            search = tag.search(root[-1].text)
            if search:
                match = search.start()
                root[-1].text = root[-1].text[:match]
            text = root[-1].text
        else:
            text = string
        char_list = list()
        for char in text:
            char_list.append(char)
    
        feature_matrix = features(char_list)
        doc_list.append(feature_matrix)
        total_features = pd.concat([total_features, feature_matrix], axis=0)

    end_train = time.time() - begin_train
    print "Done prepping training data in ", end_train, "seconds"
    end_train = time.time()
    total_features.to_csv('train_features', encoding='utf-8', sep=sep, header=False, index=False)
    save_train = time.time() - end_train
    print "Training features saved"

if 1: #If we're reformating test data at the same time.
    print "Beginning test data prep"
    begin_test = time.time()
    name = re.compile("/")
    for path in TESTDATA:
        #print path
        
        with open(path) as f:
            string = f.read()
        if path[-3:] == ".xml":
            root = etree.fromstring(string)
            tree = etree.parse(path)

            #Removes vestigial html tags at end of file.
            tag = re.compile("<start | <START")
            search = tag.search(root[-1].text)
            if search:
                match = search.start()
                root[-1].text = root[-1].text[:match]
            text = root[-1].text
        else:
            text = string
        char_list = list()
        for char in text:
            char_list.append(char)
    
        feature_matrix = features(char_list)
        idx = name.search(path).start()
        if not os.path.exists("formatted_test_data/"):
            os.mkdir("formatted_test_data")
        filename = "formatted_test_data/feature_format_"+ path[idx+1:-4]
        feature_matrix.to_csv(filename, encoding='utf-8', sep=sep, header=False, index=False)
    end_test = time.time() - begin_test
    print "Test data file prep completed in ", end_test, "seconds"

