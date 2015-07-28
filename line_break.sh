#!/bin/bash
FOLDER=$1
<<<<<<< Updated upstream
MODEL=$2
TEMPLATE=$3
=======
FEATSET=$2
MODEL=$3
TEMPLATE=$4
GOLD=$5
REBUILD=$6
>>>>>>> Stashed changes

python training_and_testing_data_prep.py $FOLDER $FEATSET
crf_learn $TEMPLATE train_features $MODEL
python test_shell_generator.py $MODEL formatted_test_data > tester.sh
./tester.sh
<<<<<<< Updated upstream
python table_to_txt.py formatted_output_data 1 0
=======
python table_to_txt.py formatted_output_data $GOLD $TEMPLATE $REBUILD
>>>>>>> Stashed changes

