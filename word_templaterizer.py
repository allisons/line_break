#!/usr/local/bin/python
from crf_formatter import feat_names, feat_options
import os.path

folder = ("templates/")
if not os.path.exists(folder):
    os.mkdir(folder)

"""
This script creates a shell script that defines a template file for crf++, for the word-based feature structure
"""
for l in range(len(feat_options)):
    feat_index = feat_options[l]
    for context in range(2, 7): 
        filename = folder+feat_names[l]+"_"+str(context)+"_template"
        file = "# "+feat_names[l] + " context = " + str(context) +"\n"
        counter = 0
        for j in range(0,len(feat_index)-1):    
            file += "# " + feat_index[j]+"\n"
            for i in range(-context,context):
                if counter < 10:
                    cntstr = "0"+str(counter)
                else: 
                    cntstr = str(counter)
                file +="U"+cntstr+":%x["+str(i)+"," +str(j)+"]\n"
                counter += 1
            with open(filename, 'wb') as f:
                f.write(file)
