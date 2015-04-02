counter = 0
for j in range(0,9):
    for i in range(-5,5):
        if counter < 10:
            cntstr = "0"+str(counter)
        else: 
            cntstr = str(counter)
        print "U"+cntstr+":%x["+str(i)+"," +str(j)+"]"
        counter += 1
    print

