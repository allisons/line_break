"""
This script creates a shell script that defines a template file for crf++
"""

feat_index = ["isAlpha", "isNumeric", "isPunct", "isUpper", "isLower", "is<sp>", "char"] #This should be kept updated with what is crf_formatter.py
counter = 0
context = 4 #Determines the default size of look-ahead and look-behind for context
for j in range(0,7):
    print "#", feat_index[j]
    #Increasing the context for case and numeric features.
    if feat_index[j] == "isUpper":
        context = 6
    if feat_index[j] == "isLower": 
        context = 6
    if feat_index[j] == "isNumeric":
        context = 6
    for i in range(-context,context):
        if counter < 10:
            cntstr = "0"+str(counter)
        else: 
            cntstr = str(counter)
        print "U"+cntstr+":%x["+str(i)+"," +str(j)+"]"
        counter += 1
    context = 4
    print

