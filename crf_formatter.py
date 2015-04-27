#!/usr/local/bin/python
from string import punctuation as punct
import pandas as pd

from pandas import DataFrame, Series

def features(char_list, gold_standard=True):
    if gold_standard:
        return features_orig(char_list)
    else:
        return features_no_gold(char_list)
        

def features_orig(char_list):
    assert isinstance(char_list, list)
    feat_index = Series(["isAlpha", "isNumeric", "isPunct", "isUpper", "is<sp>", "char", "new_line_value"])
    
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
        if char_list[i] in punct:
            featurelist.append(True)
        else:
            featurelist.append(False)
        
        #is character in uppercase?
        if char_list[i].isupper():
            featurelist.append(True)
        else:
            featurelist.append(False)
        
        if char_list[i] == " ":
            featurelist.append(True)
            char_list[i] = "<sp>"
            
        else:
            featurelist.append(False)
        if char_list[i] == "\n":
            newlineidx = i
            store = "NL"
            char_list[i] = "<sp>"
        else:
            store = "NNL"
        #Add character (at the end 'cause we changed it)
        featurelist.append(str("'"+char_list[i]+"'"))
        featurelist.append(store)
        
        features = Series(featurelist)
        feature_list_of_series.append(features)

    df = pd.concat(feature_list_of_series, axis=1)
    df.index = feat_index
    return df.T
    
def features_no_gold(char_list):
    assert isinstance(char_list, list)
    feat_index = Series(["isAlpha", "isNumeric", "isPunct", "isUpper", "index_of_previous_new_line", "is<sp>", "char"])
    
    feature_list_of_series = list()
    newlineidx = 0
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
        if char_list[i] in punct:
            featurelist.append(True)
        else:
            featurelist.append(False)
        
        #is character in uppercase?
        if char_list[i].isupper():
            featurelist.append(True)
        else:
            featurelist.append(False)
        
        if char_list[i] == " ":
            featurelist.append(True)
            char_list[i] = "<sp>"
            
        else:
            featurelist.append(False)
        #Add character (at the end 'cause we changed it)
        featurelist.append(str("'"+char_list[i]+"'"))
        
        features = Series(featurelist)
        feature_list_of_series.append(features)
        
    df = pd.concat(feature_list_of_series, axis=1)
    df.index = feat_index
    return df.T  
    