from glob import glob

test = glob("test_files/test_files/*")

print "#!/bin/bash"
for t in test:
    output = " | sed '1d' > test_files/predicted_" + t[37:-4]
    print "crf_test -v1 -m model_04_23_13 " + t + output
    
