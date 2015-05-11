#!/bin/bash
FOLDER=$1
MODEL=$2
TEMPLATE=$3
GOLD=$4
CHAR=$5

python training_and_testing_data_prep.py $FOLDER
crf_learn $TEMPLATE train_features $MODEL
python test_shell_generator.py $MODEL > tester.sh
./tester.sh
python table_to_txt.py formatted_output_data $GOLD $CHAR

