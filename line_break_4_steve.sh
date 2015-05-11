#!/bin/bash
MODEL=$1
STEVESFILE = $2
GOLD=$3
CHAR=$4


#python training_and_testing_data_prep.py $FOLDER
#crf_learn $TEMPLATE train_features $MODEL
python test_shell_generator.py $MODEL $STEVESFOLDER > tester.sh
./tester.sh
python table_to_txt.py formatted_output_data $GOLD $CHAR

