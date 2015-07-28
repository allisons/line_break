#!/usr/local/bin/python
from sklearn import svm
import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import scipy as sp

test_file = "pima_test.txt"
train_file = "pima_train.txt"
headings = ["# times preg", "glucose tolerance test", "dia bp", "skinfold thickness", "insulin", "BMI", "diabetes pedigree function", "age", "hasdiabetes?"]

train_data = pd.read_table(train_file, header=headings)
test_data = pd.read_table(test_file, header=headings)

print train_data