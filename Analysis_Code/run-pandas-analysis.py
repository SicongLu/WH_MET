'''
This is the main script for relevant pandas analysis, including:
Reading the datafrom from both .csv and .root;
Generate relevant feature;
Skim to only relevant feature;
Make correlation of features;
Use xGBoost to explore the limit of our analysis; (not for actual analysis);
'''

import pandas_analysis

from create_file_list import get_files
MC_list = get_files()

a = pandas_analysis.pandas_analyzer()

file_name = "TChiWH_700_1"
#a.set_active_branch()
#a.read_df_from_root(file_name)
#a.save_df_to_csv()
a.read_df_from_csv(file_name)
a.make_correlation_plot()
feature_list = ["mct","ptbb"]#,"ngoodjets"
a.make_scatter_matrix(feature_list)

#import sys
#print('imported')
#if len(sys.argv) < 2:
#    print('Must specify configuration file.')
#    sys.exit(1)
#print(sys.argv[1])