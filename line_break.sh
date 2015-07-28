#!/bin/bash
TRAINFILE=$1
TESTFILE=$2
FEATSET=$3
MODEL=$4
TEMPLATE=$5
GOLD=$6
REBUILD=$7

=======
python training_and_testing_data_prep.py $TRAINFILE $TESTFILE $FEATSET
crf_learn $TEMPLATE train_features $MODEL
python test_shell_generator.py $MODEL formatted_test_data > tester.sh
./tester.sh
python table_to_txt.py formatted_output_data $GOLD $TEMPLATE $REBUILD

