# line_break

The purpose of this package is to take electronic health records (EHR) from Epic that has lost (through no fault of its own) all of the new lines that indicate the structure of the record, and predict the best place for those new lines to go.  

It has been designed to run with a single call to line_break.sh and this is the usage:

Usage:
$ ./line_break.sh FOLDER_WHERE_RECORDS_LIVE NAME_OF_MODEL_YOU_WILL_CREATE TEMPLATE_YOU_CREATED 

The script will then begin by taking that set of text-only files and extracting the word features from it and outputting those features in the format required by CRF++ (more on CRF++ here http://taku910.github.io/crfpp/) - it will save the training features in a file it creates called train_features and the test feature files will be saved separately with a naming scheme based on the original (hopefully unique) names of those files.

The next step it will do is take those training features, the template you passed to it, and call CRF++'s train command and create you a model.  It'll show you its progress as it goes along.

After that model has been created, the script will use crf_test and the model to predict new labels.  It outputs the same table-format that it requires as input with the additional column for the predicted label.

The next step will be to take those predicted labels and use them to recreate the text-based files that will hopefully look like the EHR's original format and also tabulate the results.  It can optionally also create html versions of those files with highlighting to show you where the model failed and succeeded.
