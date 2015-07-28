from glob import glob
import sys
import random

rnd = random.Random()
rnd.seed(42)

#data = glob(sys.argv[1]+"/*")
data = glob("train_test_data/*")
N = len(data)
n = int(N*.1)
shuffled = rnd.sample(data, N)

print N, n