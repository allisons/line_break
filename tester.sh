#!/bin/bash
crf_test -v1 -m model_04_23_13 test_files/test_files/feature_format_report0.csv | sed '1d' > test_files/predicted_report0
crf_test -v1 -m model_04_23_13 test_files/test_files/feature_format_report10.csv | sed '1d' > test_files/predicted_report10
crf_test -v1 -m model_04_23_13 test_files/test_files/feature_format_report100000.csv | sed '1d' > test_files/predicted_report100000
crf_test -v1 -m model_04_23_13 test_files/test_files/feature_format_report100010.csv | sed '1d' > test_files/predicted_report100010
crf_test -v1 -m model_04_23_13 test_files/test_files/feature_format_report100020.csv | sed '1d' > test_files/predicted_report100020
crf_test -v1 -m model_04_23_13 test_files/test_files/feature_format_report100030.csv | sed '1d' > test_files/predicted_report100030
crf_test -v1 -m model_04_23_13 test_files/test_files/feature_format_report100040.csv | sed '1d' > test_files/predicted_report100040
crf_test -v1 -m model_04_23_13 test_files/test_files/feature_format_report100050.csv | sed '1d' > test_files/predicted_report100050
crf_test -v1 -m model_04_23_13 test_files/test_files/feature_format_report20.csv | sed '1d' > test_files/predicted_report20
crf_test -v1 -m model_04_23_13 test_files/test_files/feature_format_report30.csv | sed '1d' > test_files/predicted_report30
crf_test -v1 -m model_04_23_13 test_files/test_files/feature_format_report40.csv | sed '1d' > test_files/predicted_report40
crf_test -v1 -m model_04_23_13 test_files/test_files/feature_format_report60.csv | sed '1d' > test_files/predicted_report60
crf_test -v1 -m model_04_23_13 test_files/test_files/feature_format_report70.csv | sed '1d' > test_files/predicted_report70
crf_test -v1 -m model_04_23_13 test_files/test_files/feature_format_report80.csv | sed '1d' > test_files/predicted_report80
