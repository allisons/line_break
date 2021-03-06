from glob import glob
import sys
import random
import pickle

rnd = random.Random()
rnd.seed(42)

#data = glob(sys.argv[1]+"/*")
data = glob("train_test_data/*")
N = len(data)
n = int(N*.1)
shuffled = rnd.sample(data, N)

for i in xrange(10):
    with open("10_folds/training_fold_"+str(i)+".txt", 'w') as tr:
        train = shuffled[0:i] + shuffled[i+n:]
        for path in train:
                tr.write(path+"\n")
    with open("10_folds/testing_fold_"+str(i)+".txt", 'w') as ts:
        test = shuffled[i:i+n]
        for path in test:
            ts.write(path+"\n")