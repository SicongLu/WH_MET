# Relevant info
create_file_list.py and selection_criteria.py is the same as in ../Analysis_Code/ .

# Main analysis frame work
pandas_analysis.py is responsible for all analysis functions, including:
the transformation between .root, pandas dataframe, .csv, numpy array, etc. It will also save the .csv file to ../csv_file_temp/ .

run-pandas-analysis.py controls it.


# Testing...
One is now using the following code to learn xgboost:
test_xgb.py