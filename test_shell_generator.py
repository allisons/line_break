from glob import glob
import sys
import os.path
import re

model = sys.argv[1]
test = sys.argv[2] + "/*"
test = glob(test)
if not os.path.exists("formatted_output_data/"):
    os.mkdir("formatted_output_data")
name = re.compile("/")

print "#!/bin/bash"
for t in test:
    idx = name.search(t).start()
    output = " | sed '1d' > formatted_output_data" + t[idx:]
    print "crf_test -v1 -m " +  model +" "+ t + output
    
