#!/bin/bash
FOLDER=$1
MODEL=$2
TEMPLATE=$3

#python training_and_testing_data_prep.py $FOLDER
#crf_learn -c 1.5 $TEMPLATE train_features $MODEL
python test_shell_generator.py $MODEL > tester.sh
./tester.sh
python table_to_txt.py formatted_output_data 1

