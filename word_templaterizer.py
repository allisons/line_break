"""
This script creates a shell script that defines a template file for crf++, for the word-based feature structure
"""
feat_index = ["word", "isalpha", "allcaps", 'lowercase', 'titlecase', 'endsWithPunctuation', "startsWithPunctuation", "hasNumbers", "allNum", "new_line_value"]
counter = 0
context = 4 
for j in range(0,len(feat_index)-1):
    print "#", feat_index[j]
    #Increasing the context for case and numeric features.
    for i in range(-context,context):
        if counter < 10:
            cntstr = "0"+str(counter)
        else: 
            cntstr = str(counter)
        print "U"+cntstr+":%x["+str(i)+"," +str(j)+"]"
        counter += 1
    context = 4
    print

