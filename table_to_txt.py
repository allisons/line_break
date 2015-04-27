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

#paths = glob("test_files/predicted*")
paths = list(glob(sys.argv[1]))
    

folder = ("output_files/")
#os.mkdir(folder)

def rebuild(table, output_name):
    print table
    rebuild = ""
    characters = table.iloc[:,6]
    newlines = table.iloc[:,7]
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
    gold = table.iloc[:,6]
    yhat = table.iloc[:,7]
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
                #this is true neg
                count = results.at["TN", "count"]
                mean = results.at["TN", "mean prob"]
                results.at["TN", "count"] = count + 1
                results.at["TN", "mean prob"] = mean + prob
        elif yhat == "NNL":
            #this is a false negative
            count = results.at["FN", "count"]
            mean = results.at["FN", "mean prob"]
            results.at["FN", "count"] = count + 1
            results.at["FN", "mean prob"] = mean + prob
        else:
            count = results.at["TP", "count"]
            mean = results.at["TP", "mean prob"]
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
    print table
    new = tabulate_results(table)
    total += new
    count +=1
    #rebuild(table, outputname)

total['mean prob'] = total['mean prob']/count
#print total

p = total.at['TP', 'count']/(total.at['TP', 'count']+total.at['FP', 'count'])
r = total.at['TP', 'count']/(total.at['TP', "count"]+total.at['FN', 'count'])
f = 2*(p*r)/(p+r)
#print 'precision =', p, "recall =", r, "f-score=", f