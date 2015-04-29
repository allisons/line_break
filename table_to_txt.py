#!/usr/local/bin/python
from __future__ import division
import pandas as pd
from pandas import DataFrame, Series
import numpy as np
from lxml import etree
import re
from string import punctuation as punct
import os.path
from glob import glob
from collections import defaultdict
from functools import partial
import sys

"""
This script takes a list of files that are the output of crf_test and if they
have oracle labels, calculates the precision, recall and f-score and prints those
to standard output and for all inputs produces a file with the predicted newlines 
based on the file names passed  to it and places it in the "output_files" folder.  
It creates that folder if it does not currently exist.
"""

paths = sys.argv[1]
gold_standard = bool(sys.argv[2])
paths = sys.argv[1] + "/*"
paths = glob(paths)

folder = ("output_files/")
if not os.path.exists(folder):
    os.mkdir(folder)
    
print "Rebuilding text files with predicted new lines"
if gold_standard:
    print "    and tabulating results from test data"

def rebuild(table, output_name, gold_standard=True):
    rebuild = ""
    if gold_standard:
        characters = table.iloc[:,-3]
    else:
        characters = table.iloc[:,-2]
    newlines = table.iloc[:,-1]
    for char, new in zip(characters.iteritems(), newlines.iteritems()):
        _, c = char
        _, nl = new
        if 1: #We're using a verbose version of the output
            label, _ = nl.split("/")
            nl = label
        if nl == "NL":
            rebuild +="\n"
        elif c == "'<sp>'":
            rebuild += " "
        else:
            rebuild += c[1:-1]
    with open(output_name, 'wb') as new:
         new.write(rebuild)
        
def tabulate_results(table):
    assert gold_standard == 1 #need an oracle to tablulate results!
    
    gold = table.iloc[:,-2]
    yhat = table.iloc[:,-1]
    results = DataFrame(np.zeros(shape=(4,2)), dtype=float)
    results.index=("TP", "FN", "FP", "TN")
    results.columns=("count", "mean prob")
    
    for a, b in zip(gold.iteritems(), yhat.iteritems()):
        _, y = a
        _, result = b
        yhat, prob = result.split("/")
        prob = float(prob)
        if y == yhat:
            if y == "NL":
                #This is a true pos
                count = results.at["TP", "count"]
                mean = float(results.at["TP", "mean prob"])
                results.at["TP", "count"] = count + 1
                results.at["TP", "mean prob"] = mean + prob
            else:
                assert y == "NNL"
                #this is true neg
                count = results.at["TN", "count"]
                mean = results.at["TN", "mean prob"]
                results.at["TN", "count"] = count + 1
                results.at["TN", "mean prob"] = mean + prob
        elif yhat == "NNL":
            assert y == "NL"
            #this is a false negative
            count = results.at["FN", "count"]
            mean = results.at["FN", "mean prob"]
            results.at["FN", "count"] = count + 1
            results.at["FN", "mean prob"] = mean + prob
        else:
            #This is a false positive
            assert yhat == "NL"
            assert y == "NNL"
            count = results.at["FP", "count"]
            mean = results.at["FP", "mean prob"]
            results.at["FP", "count"] = count + 1
            results.at["FP", "mean prob"] = mean + prob        
    results.at["TP", "mean prob"] /= results.at["TP", "count"]
    results.at["FN", "mean prob"] /= results.at["FN", "count"]
    results.at["FP", "mean prob"] /= results.at["FP", "count"]
    results.at["TN", "mean prob"] /= results.at["TN", "count"]
    
    return results
total = DataFrame(np.zeros(shape=(4,2)), dtype=float)
total.index=("TP", "FN", "FP", "TN")
total.columns=("count", "mean prob")
count = 0

for p in paths:
    filename = p.split("/")
    filename = filename[-1]
    outputname = folder+filename
    table = pd.read_table(p, header=None)
    if gold_standard:
        new = tabulate_results(table)
        total += new
        count +=1
    rebuild(table, outputname)

if gold_standard:
    total['mean prob'] = total['mean prob']/count
    TP = total.at['TP', 'count']
    TN = total.at['TN', 'count']
    FN = total.at['FN', 'count']
    FP = total.at['FP', 'count']
    cnfmat = DataFrame(np.zeros(shape=(3,3)), dtype=float)
    cnfmat.columns=("Oracle True", "Oracle False", "Total")
    cnfmat.index=("Predicted True", "Predicted False", "Total")
    cnfmat.at["Predicted True", "Oracle True"] = TP
    cnfmat.at["Predicted False", "Oracle False"] = TN
    cnfmat.at['Predicted True', "Oracle False"] = FP
    cnfmat.at["Predicted False", "Oracle True"] = FN
    cnfmat.at["Predicted True", "Total"] = TP + FP
    cnfmat.at["Predicted False", "Total"] = FN + TN
    cnfmat.at["Total", "Oracle True"] = TP+FN
    cnfmat.at["Total", "Oracle False"] = TN+FP
    cnfmat.at["Total", "Total"] = TP + FN + FP + TN
    print cnfmat
    p = TP/(TP + FP)
    r = TP/(TP + FN)
    f = 2*(p*r)/(p+r)
    print 'precision =', p, "recall =", r, "f-score=", f