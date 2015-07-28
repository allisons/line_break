#!/bin/bash
MODEL=$1
FOLDER = $2
#FEAT_CLASS = $3

python text_to_test_file_format.py $FOLDER allword
python test_shell_generator.py $MODEL formatted_test_data > tester.sh
chmod +x tester.sh
./tester.sh
python table_to_txt.py formatted_output_data 0 0


#FILES YOU NEED
#text_to_test_file_format.py
#test_shell_genator.py
#table_to_txt.py