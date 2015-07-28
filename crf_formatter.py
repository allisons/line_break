#!/usr/local/bin/python
from string import punctuation as punct
import pandas as pd
import re

from pandas import DataFrame, Series

CHAR_FEAT_LIST = ["isAlpha", "isNumeric", "isPunct", "isUpper", "isLower", "is<sp>", "char", "new_line_value"]
WORD_FEAT_LIST = ["word", "isalpha", "allcaps", 'lowercase', 'titlecase', 'endsWithPunctuation', 
"startsWithPunctuation", "hasNumbers", "allNum", "new_line_value"]
CASE_FEAT =["word", "isalpha", "allcaps", "lowercase", "titlecase", "new_line_value"]
NUM_FEAT = ["word", "isalpha", "hasNumbers", "allNum", "new_line_value"]
PUNCT_FEAT =["word", "isalpha", "endsWithPunctuation", "startsWithPunctuation", "new_line_value"]
CASE_NUM_FEAT = ["word", "isalpha", "allcaps", "lowercase", "titlecase", "hasNumbers", "allNum", "new_line_value"]
CASE_PUNCT_FEAT = ["word", "isalpha", "allcaps", "lowercase", "titlecase", "endsWithPunctuation", "startsWithPunctuation", "new_line_value"]
NUM_PUNCT_FEAT = ["word", "isalpha", "hasNumbers", "allNum","endsWithPunctuation", "startsWithPunctuation", "new_line_value"]

feat_options = [WORD_FEAT_LIST, CASE_FEAT, NUM_FEAT, PUNCT_FEAT, CASE_NUM_FEAT, CASE_PUNCT_FEAT, NUM_PUNCT_FEAT]
feat_names = ["AllWordFeatures", "CaseFeatures", "NumFeatures", "PunctuationFeatures", "CaseandNumFeatures", "CaseandPunctFeatures", "NumandPunctFeatures"]

def char_features(char_list, gold_standard=True):
    assert isinstance(char_list, list)
    
    #If the data contains an oracle label, include that label in the features table
    if gold_standard:
        feat_index = Series(CHAR_FEAT_LIST)
    else:
        feat_index = Series(CHAR_FEAT_LIST[:-1])
    
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
    
def word_features(text, gold_standard=True):
    feature_list_of_features = list()
    if gold_standard:
        feat_index = Series(WORD_FEAT_LIST)
    else:
        feat_index = Series(WORD_FEAT_LIST[:-1])
    
    paragraphs = text.split("\n")
    for p in paragraphs:
        words = p.split()
        linelen = len(words)
        if linelen == 0:
            feature_list = ["<BLANKLINE>", False, True, True, False, False, False, False, False, True]
        pointer = 1
        for w in words:
            feature_list = list()
            #Add word itself
            feature_list.append(w)
            
            #If the word isalpha()
            if w.isalpha():
                feature_list.append(True)
            else:
                feature_list.append(False)
            
            #if word is all caps
            if w.isupper():
                feature_list.append(True)
            else:
                feature_list.append(False)
            
            #if word is lowercase
            if w.islower():
                feature_list.append(True)
            else:
                feature_list.append(False)
                
            #is word titlecase?
            if w[0].isupper() and w[1:].islower():
                feature_list.append(True)
            else:
                feature_list.append(False)
            
            #Ends in punctuation
            if w[-1] in punct:
                feature_list.append(True)
            else:
                feature_list.append(False)
            
            if w[0] in punct:
                feature_list.append(True)
            else:
                feature_list.append(False)
            
            #Has digits
            nodigit = True
            for idx in range(len(w)):
                if w[idx].isdigit():
                    feature_list.append(True)
                    nodigit = False
                    break
            if nodigit:
                feature_list.append(False)
            
            #Is only digits:
            if w.isdigit():
                feature_list.append(True)
            else:
                feature_list.append(False)
            if gold_standard:
                if pointer == linelen:
                    feature_list.append("NL")
                else:
                    feature_list.append("NNL")
                    pointer += 1
            features = Series(feature_list)
            feature_list_of_features.append(features)
        
    df = pd.concat(feature_list_of_features, axis=1)
    df.index = feat_index
    return df.T
    


def case_features(text, gold_standard=True):
    all_feat = word_features(text, gold_standard)
    return all_feat[CASE_FEAT]

def num_features(text, gold_standard=True):
    all_feat = word_features(text, gold_standard)
    return all_feat[NUM_FEAT]

def punct_features(text, gold_standard=True):
    all_feat = word_features(text, gold_standard)
    return all_feat[PUNCT_FEAT]
    
def case_num_features(text, gold_standard=True):
    all_feat = word_features(text, gold_standard)
    return all_feat[CASE_NUM_FEAT]

def case_punct_features(text, gold_standard=True):
    all_feat = word_features(text, gold_standard)
    return all_feat[CASE_PUNCT_FEAT]

def num_punct_features(text, gold_standard=True):
    all_feat = word_features(text, gold_standard)
    return all_feat[NUM_PUNCT_FEAT]

def my_split(text, pattern):
    text_list = list()
    nl = re.compile(pattern)
    while len(text) > 0:
        search = nl.search(text)
        if search:
            s = search.start()
            e = search.end()
            text_list.append(text[s+1:e-1])
            text = text[e:]
        else:
            text_list.append(text)
            text = ""
    return text_list

