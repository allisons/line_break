#!/usr/local/bin/python
from __future__ import division
import pandas as pd
from pandas import DataFrame, Series
from lxml import etree
import re
from string import punctuation as punct
import os.path
from glob import glob

file = "results_file"

results = pd.read_table(file, header=None)


characters = results.iloc[:,6]
gold = results.iloc[:, 7]
newlines = results.iloc[:,8]

rebuild = ""
for char, new in zip(characters.iteritems(), newlines.iteritems()):
    _, c = char
    _, nl = new
    if nl == "NL":
        rebuild +="\n"
    elif c == "<sp>":
        rebuild += " "
    else:
        rebuild += c

with open("new_file.txt", 'wb') as new:
     new.write(rebuild)

TP = 0
TN = 0
FP = 0
FN = 0
falsenegidx=list()

for a, b in zip(gold.iteritems(), newlines.iteritems()):
    _, y = a
    idx, yhat = b
    if y == yhat:
        if y == "NNL":
            TN += 1
        else:
            TP += 1
    elif y == "NNL":
        FP += 1
    else:
        FN += 1
        falsenegidx.append(idx)
        
print "TP is", TP
print "TN is", TN
print "FP is", FP
print "FN is", FN

df = DataFrame([[TP, FP], [FN, TN]], index=("Yhat NL", "Yhat NNL"), columns=("Y NL", "Y NNL"))
print df

print "precision=", TP/(TP+FP)
print "recall=", TP/(TP+FN)

print falsenegidx