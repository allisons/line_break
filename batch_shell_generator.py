#!/usr/local/bin/python
from crf_formatter import *
from glob import glob
import os.path

feat_functs = {"case": case_features, "num": num_features, "punct": punct_features, "casenum": case_num_features, 
"casepunct": case_punct_features, "numpunct": num_punct_features, "allword": word_features}

folder1 = "formatted_output_data"
folder2 = "formatted_test_data"
folder3 = "output_files"
file = "train_features"

templates = glob("templates/*")
call = "./line_break.sh"
folder = "train_test_data"
feat_sets = ["allword", "casenum", "casepunct", "case", "numpunct", "num", "punct"]
i = 0

for t in templates:
    it = 0
    for _ in range(10):
        print "rm -rf", folder1
        print "rm -rf", folder2
        print "rm -rf", folder3
        print "rm", file
        print call, folder, feat_sets[i/5], t[10:-8]+"model"+"_"+str(it), t, 1, 0
        it += 1
    i += 1
    print "rm", t[10:-8]+"model*"
print "rm -rf", folder1
print "rm -rf", folder2
print "rm -rf", folder3
print "rm", file        
    