#!/usr/local/bin/python
from __future__ import division
import pandas as pd
from pandas import DataFrame, Series
from lxml import etree
import re
from string import punctuation as punct
import os.path
from glob import glob
import sys

sep = "\t"

if 0:
    TESTDATA = glob(sys.argv[1])
    TRAINDATA = glob(sys.argv[2])

else:
    TRAINDATA1 = glob('sliter_gold_standard/*')
    TRAINDATA2 = glob('first_50/*')
    TRAINDATA = TRAINDATA1 + TRAINDATA2
    TESTDATA = glob('test_files/*')

def features(text): #Give this as a list of characters, rather than a single string (so we can take a " " or "\n" and return it as a "<sp>")
    assert isinstance(text, list)
    feat_index = Series(["isAlpha", "isNumeric", "isPunct", "isUpper", "index_of_previous_new_line", "is<sp>", "char", "new_line_value"])
    
    feature_list_of_series = list()
    newlineidx = 0
    for i in range(len(text)):
        featurelist = list()    
        
        #is character alpha?
        if text[i].isalpha():
            featurelist.append(True)
        else:
            featurelist.append(False)
        
        #is character a digit?
        if text[i].isdigit():
            featurelist.append(True)
        else:
            featurelist.append(False)
        
        #is character punctuation?
        if text[i] in punct:
            featurelist.append(True)
        else:
            featurelist.append(False)
        
        #is character in uppercase?
        if text[i].isupper():
            featurelist.append(True)
        else:
            featurelist.append(False)
        
        featurelist.append(newlineidx//20 * 20)
        if text[i] == " ":
            featurelist.append(True)
            text[i] = "<sp>"
            
        else:
            featurelist.append(False)
        if text[i] == "\n":
            newlineidx = i
            store = "NL"
            text[i] = "<sp>"
        else:
            store = "NNL"
        #Add character (at the end 'cause we changed it)
        featurelist.append(text[i])
        featurelist.append(store)
        
        
            
        
        features = Series(featurelist)
        feature_list_of_series.append(features)

    df = pd.concat(feature_list_of_series, axis=1)
    df.index = feat_index
    return df.T               
        

if 1: #prepping training data
    total_features = DataFrame()
    doc_list = list()
    for path in TRAINDATA:
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
        x = len(text)
        char_list = list()
        for char in text:
            char_list.append(char)
    
        feature_matrix = features(char_list)
        doc_list.append(feature_matrix)
        total_features = pd.concat([total_features, feature_matrix], axis=0)

    total_features.to_csv('train_features.csv', encoding='utf-8', sep=sep, header=False, index=False)


if 1: #If we're reformating test data at the same time.
    name = re.compile("/")
    for path in TESTDATA:
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
        x = len(text)
        char_list = list()
        for char in text:
            char_list.append(char)
    
        feature_matrix = features(char_list)
        idx = name.search(path).start()
        filename = "test_files/feature_format_"+ path[idx+1:-3]+"csv"
        feature_matrix.to_csv(filename, encoding='utf-8', sep=sep, header=False, index=False)
    






