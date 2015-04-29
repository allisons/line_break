#!/usr/local/bin/python
from string import punctuation as punct
import pandas as pd

from pandas import DataFrame, Series

FEAT_LIST = ["isAlpha", "isNumeric", "isPunct", "isUpper", "isLower", "is<sp>", "char", "new_line_value"]
"""
This module takes a list of characters and returns  a pandas DataFrame 
containing the features data.  Most of the features are boolean, however
 the 7th (index 6)  column stores the character itself both as a feature 
 and also to make it possible to reconstruct a text file with the new 
 formatting at the end of the process.  This module should not be run 
 directly, instead it should be called by a script that pre-processes a text
 file into the character list format
"""

def features(char_list, gold_standard=True):
    assert isinstance(char_list, list)
    
    #If the data contains an oracle label, include that label in the features table
    if gold_standard:
        feat_index = Series(FEAT_LIST)
    else:
        feat_index = Series(FEAT_LIST[:-1])
    
    feature_list_of_series = list()
    for i in range(len(char_list)):
        featurelist = list()    
        
        #is character alpha?
        if char_list[i].isalpha():
            featurelist.append(True)
        else:
            featurelist.append(False)
        
        #is character a digit?
        if char_list[i].isdigit():
            featurelist.append(True)
        else:
            featurelist.append(False)
        
        #is character punctuation?
        if char_list[i] in punct and not ((char_list[i] is '*') or (char_list[i] is '[') or (char_list[i] is ']')):
            featurelist.append(True)
        else:
            featurelist.append(False)
        
        #is character in uppercase?
        if char_list[i].isupper():
            featurelist.append(True)
        else:
            featurelist.append(False)
            
        #is character in lowercase?
        if char_list[i].islower():
            featurelist.append(True)
        else:
            featurelist.append(False)
        
        
        if (char_list[i] == " "):
            featurelist.append(True)
            char_list[i] = "<sp>"
            store = "NNL"
            
        elif char_list[i] =="\n":
            if gold_standard:
                char_list[i] = "<sp>"
                featurelist.append(True)
                char_list[i] = "<sp>"
                store = "NL"
            else:
                featurelist.append(False)
        else:
            featurelist.append(False)
            store = "NNL"
        #Add character (at the end 'cause we changed it)
        featurelist.append(str("'"+char_list[i]+"'"))
        
        #Add oracle label
        if gold_standard:
            featurelist.append(store)
        
        features = Series(featurelist)
        feature_list_of_series.append(features)

    df = pd.concat(feature_list_of_series, axis=1)
    df.index = feat_index
    return df.T
    
