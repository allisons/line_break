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
GOLD_STANDARD = "1" == sys.argv[2]
paths = sys.argv[1] + "/*"
paths = glob(paths)
template = sys.argv[3].split("/")[-1]
REBUILD = sys.argv[4] == "1"


assert (REBUILD or GOLD_STANDARD) #If both are false, I have nothing to do.

folder = ("output_files/")
if REBUILD:
    if not os.path.exists(folder):
        os.mkdir(folder)
    html_folder = ("html_error_viz/")
    if not os.path.exists(html_folder):
        os.mkdir(html_folder)

    
if REBUILD:
    print "Rebuilding text files with predicted new lines"
if GOLD_STANDARD:
    print "Tabulating results from test data"

def color_code_rebuild(table, output_name):
    header = "<html>\n<head></head><body>\n<p>"
    rebuild = ""
    falsepos = 0
    falseneg = 0
    words = table.iloc[:,0]
    oracle = table.iloc[:,-2]
    newlines = table.iloc[:, -1]
    for word, oracle, new in zip(words.iteritems(), oracle.iteritems(), newlines.iteritems()):
        _, w = word
        _, true = oracle
        _, nl = new
        label, _ = nl.split("/")
        nl = label
        if nl =="NL" and true == "NL":
            if w == "<BLANKSPACE>":
                rebuild += "-|-</p><p>"
            else:
                rebuild += str(w) + "</p><p>"
        elif nl == "NL" and true == "NNL":
            falsepos += 1
            rebuild += "</p><SPAN STYLE=\"background-color:#AA5585\">[ ]</SPAN><p>"
        elif nl == "NNL" and true == "NL":
            rebuild += str(w) + "<SPAN STYLE=\"background-color:#A5C663\"> </SPAN> "
            falseneg += 1
        else:
            rebuild += str(w) + " "
        
    rebuild += "<p>\n</body></html>"
    rebuild = header + "<p>Missed NewLine count = <SPAN STYLE=\"background-color:#A5C663\">" + str(falseneg) + "</SPAN> Extra NewLine count = <SPAN STYLE=\"background-color:#AA5585\">" + str(falsepos) + "</SPAN> </p><p>" + rebuild
    output_name += ".html"
    with open(output_name, 'wb') as out:
        out.write(rebuild)
    

def rebuild(table, output_name, gold_standard=True):
    rebuild = ""
    words = table.iloc[:,0]
    if gold_standard:
        character = table.iloc[:,-3]
    else:
        character = table.iloc[:,-2]
    newlines = table.iloc[:,-1]
    for word, new in zip(words.iteritems(), newlines.iteritems()):
        _, w = word
        _, nl = new
        if 1:
            label, _ = nl.split("/")
            nl = label
        if nl == "NL":
            if w == "<BLANKSPACE>":
                rebuild += "\n"
            else:
                rebuild += str(w) + "\n"
        else:
            rebuild += str(w) + " "
    with open(output_name, 'wb') as new:
         new.write(rebuild)
        
def tabulate_results(table):
    assert GOLD_STANDARD == 1 #need an oracle to tablulate results!
    
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
    filename = "reconstructed_" + filename[-1][15:]
    outputname = folder+filename
    table = pd.read_table(p, header=None)
    if REBUILD:
        rebuild(table, outputname)
    if GOLD_STANDARD:
        new = tabulate_results(table)
        total += new
        count +=1
        if REBUILD:
            htmloutput = html_folder+filename
            color_code_rebuild(table, htmloutput)

if GOLD_STANDARD:
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
    p = TP/(TP + FP)
    r = TP/(TP + FN)
    f = 2*(p*r)/(p+r)
    line = template + "\t" + str(TP) + "\t" + str(FP) + "\t" + str(FN) + "\t" + str(TN) + "\t" + str(p) + "\t" + str(r) + "\t" + str(f) +"\n"
    with open("totalresults.txt", "a") as f:
        f.write(line)
