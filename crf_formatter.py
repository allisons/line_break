#!/usr/local/bin/python
from string import punctuation as punct
import pandas as pd
import re

from pandas import DataFrame, Series

file = "report100001.txt"

CHAR_FEAT_LIST = ["isAlpha", "isNumeric", "isPunct", "isUpper", "isLower", "is<sp>", "char", "new_line_value"]
WORD_FEAT_LIST = ["word", "isalpha", "allcaps", 'lowercase', 'titlecase', 'endsWithPunctuation', "startsWithPunctuation", "hasNumbers", "allNum", "new_line_value"]

"""
This module takes a list of characters and returns  a pandas DataFrame 
containing the features data.  Most of the features are boolean, however
 the 7th (index 6)  column stores the character itself both as a feature 
 and also to make it possible to reconstruct a text file with the new 
 formatting at the end of the process.  This module should not be run 
 directly, instead it should be called by a script that pre-processes a text
 file into the character list format
"""

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
    
    
with open(file, 'rb') as f:
    text = f.read()

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

test_text = """Report de-identified (Safe-harbor compliant) by De-ID v.6.22.08.0]
 
 
**INSTITUTION
ORTHOPEDIC SURGERY
OPERATIVE REPORT  
PATIENT NAME:  **NAME[AAA, BBB M]
ACCOUNT #:  **ID-NUM
**ROOM
SURGEON:  **NAME[WWW XXX], M.D.
ASSISTANT(S):  **NAME[RRR QQQ], M.D.
 
ATTENDING PHYSICIAN:  **NAME[ZZZ M YYY]
SURGERY DATE:  **DATE[Nov 27 05]
ADMISSION DATE:  **DATE[Nov 22 2007]
DISCHARGE DATE:  
   
PROCEDURES:  
 
TITLE OF OPERATION:  IRRIGATION AND DEBRIDEMENT OF LEFT KNEE.
 
ANESTHESIA:  General.  
COMPLICATIONS:  None.  
PREOPERATIVE DIAGNOSIS(ES):  SEPTIC ARTHRITIS, LEFT KNEE.
 
POSTOPERATIVE DIAGNOSIS(ES):  SEPTIC ARTHRITIS, LEFT KNEE.
 
HISTORY AND INDICATIONS:  The patient is a **AGE[in 60s]-year-old female with a history of end-stage renal disease and hemodialysis with vasculopathy who by history, examination, and laboratory studies had a septic arthritis of the left knee.   
Preoperatively, I spoke to the patient at great length.  I spoke to her and her daughter about the risks and benefits of surgical intervention.  We talked about complications of anesthesia, septic arthritis, continued pain, neurovascular surgery, need for future surgeries, soft tissue complications etc.  I explained to that irrigation and debridement of septic arthritis is indicated and we talked about this at great length.  After thorough a discussion about the risks and benefits of surgery, the patient gave informed consent.   
DESCRIPTION OF OPERATION:  The patient was identified as the patient.  She was taken to the operating room where she was placed supine on a table.  Anesthesia had attempted to place a block; however, this did not work and therefore she  needed to be intubated.  After successful intubation, a nonsterile tourniquet was carefully placed high in the left thigh.  The left leg was then prepped and draped in the usual sterile fashion while making sure to isolate the left foot on which she had surgery a few days prior.  The leg was elevated for 120 seconds and then the tourniquet was inflated.  A small approximately 5 cm parapatellar arthrotomy was performed sharply with a knife.  This was taken down into the joint sharply.  Immediately significant amount of cloudy-looking fluid came out of the knee.  This was sent for culture.  After evacuating the fluid, the knee was pulse irrigated with 3 L of solution.  After this, we reexamined the knee.  There was no further sign of purulence.  The skin bleeders were coagulated.  Again, 3 more liters of pulse irrigation were used to clean out the knee.  After successfully accomplishing this, the arthrotomy was closed with 0 Vicryl in a watertight fashion.  The skin was then closed carefully with interrupted 3-0 nylon sutures.  A sterile consisting of Xeroform, 4x4's, Webril, and Ace wrap were applied.   
The patient was awakened from anesthesia.  Earlier the tourniquet had been deflated prior to closure.   
There were no complications during this procedure.  She was brought to the PACU in a stable condition.   
     
___________________________________
**NAME[WWW XXX], M.D.
 
   
 
Dictator:  **NAME[WWW XXX], M.D.
 
MK/ga  
D:  **DATE[Nov 27 2007] 18:23:27
T:  **DATE[Nov 28 2007] 09:54:34
R:  **DATE[Nov 28 2007] 09:54:34/ga  
Job ID:  364732/**ID-NUM  
Cc: t [Report de-identified (Safe-harbor compliant) by De-ID v.6.22.06.0]
 
 
**INSTITUTION 
EMERGENCY DEPARTMENT
PATIENT NAME:  **NAME[AAA, BBB M]
ACCOUNT #:  **ID-NUM
DATE OF SERVICE:  **DATE[Feb 01 06]
PRIMARY CARE PHYSICIAN: MEDICAL  **NAME[TTT]
CHIEF COMPLAINT:
Tooth pain.
HISTORY OF PRESENT ILLNESS:  
This is a **AGE[in 20s]-year-old gentleman with a history of facial reconstructive surgery following an MVA back in 2003, who presents to the emergency department complaining of right upper tooth pain.  The patient states that, yesterday, he was at work and got hit in the jaw with a hoist.  The patient states that his tooth broke off.  Throughout the day, he began having more and more severe pain in the right upper jaw.  He was unable to eat anything today secondary to the pain.  He denies any pain in the remainder of the jaw, ear, or sinus area.  He denies any fevers or chills.  He denies any recent illnesses.  He denies any chest pain or shortness of breath.   
PAST MEDICAL HISTORY:   
Facial reconstructive surgery following a motor vehicle accident in 2003.
MEDICATIONS:
None.
ALLERGIES:
NO KNOWN DRUG ALLERGIES.
SOCIAL HISTORY:
The patient smokes about one-half pack per day.  He denies any other drug or alcohol use. 
REVIEW OF SYSTEMS:
Review of systems is negative except for those in the HPI.
PHYSICAL EXAM:  
His vital signs are stable.  His temperature is 36.7.  The rest of his vitals were stable. 
General:  He is awake, alert, and oriented times three, in no acute distress. 
HEENT examination revealed a broken first molar on the right upper jaw.  This is tender to palpation.  He also had some tenderness over the outer gum line as well as the inner gum line.  There is no obvious bleeding or drainage from the area.  He denied any tenderness along the remainder of the jaw.  There is also a small superficial abrasion on the outer corner of the bottom lip.   
Cardiac:  Regular rate and rhythm.  S1, S2.  No murmurs, rubs, or gallops.
Lungs:  Clear to auscultation bilaterally.
ED COURSE:  
This is a **AGE[in 20s]-year-old gentleman, who comes in with right tooth pain after being hit in the face by a hoist yesterday.  OMFS came down to evaluate the patient and felt that he could be discharged and would need to be followed up with a regular dentist to perhaps have that tooth pulled.  The patient was given Percocet for pain.  He was also given a prescription for Pen VK 500 mg q.i.d. times ten days since there were some roots that were exposed.   
PLAN/FOLLOW-UP: 
The patient was discharged home in stable condition.  He is to follow up with the **INSTITUTION within the next one to four days to have the tooth evaluated.   
The case was discussed with Dr. **NAME[WWW], who is in agreement with the plan.  
___________________________________
**NAME[CCC WWW], M.D.
 
Dictator:  **NAME[WWW XXX], M.D.
**INITIALS
D:  **DATE[Feb 01 2007] 22:08:18
T:  **DATE[Feb 02 2007] 07:01:00
R:  **DATE[Feb 02 2007] 07:01:00/jlw Job ID:  328064/**ID-NUM
Cc:  
*** Dictated By: -**NAME[XXX, SSS] ***
Electronically Signed by **NAME[CCC WWW]  **DATE[Feb 04 2007] 11:03:47 AM    

"""
