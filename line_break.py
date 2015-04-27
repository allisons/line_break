#!/usr/local/bin/python
from __future__ import division
import pandas as pd
from pandas import DataFrame, Series
from lxml import etree
import re
import time

from string import punctuation as punct
import os.path
from glob import glob
import sys

from crf_formatter import features

start = time.time()
sep = "\t"

if 0:
    TESTDATA = glob(sys.argv[1])
    TRAINDATA = glob(sys.argv[2])

else:
    TRAINDATA1 = glob('sliter_gold_standard/*')
    TRAINDATA2 = glob('first_50/*')
    TRAINDATA = TRAINDATA1 + TRAINDATA2
    TESTDATA = glob('test_files/*')

if 1: #prepping training data
    print "Beginning training"
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
    print "Done training in ", end_train, "seconds"
    end_train = time.time()
    total_features.to_csv('train_features.csv', encoding='utf-8', sep=sep, header=False, index=False)
    save_train = time.time() - end_train
    print "Training features saved", save_train, "seconds"

if 1: #If we're reformating test data at the same time.
    print "Beginning test data prep"

    name = re.compile("/")
    testcount = 1
    for path in TESTDATA:
        print path
        begin_test = time.time()
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
        filename = "test_files/feature_format_"+ path[idx+1:-3]+"csv"
        feature_matrix.to_csv(filename, encoding='utf-8', sep=sep, header=False, index=False)
        end_test = time.time() - begin_test
        print "Test data file", testcount, "completed in ", end_test, "seconds"
        testcount += 1
    
if 0: #Formatting debug block
    testfile = "report0.xml"
    with open(testfile, 'r') as test:
        string = test.read()
        root = etree.fromstring(string)
        tree = etree.parse(testfile)

    #Reoves vestigial html tags at end of file.
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
    print feature_matrix