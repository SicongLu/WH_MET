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
a = pandas_analysis.pandas_analyzer()
a.set_active_branch()

MC_list = get_files()
for MC in MC_list:
    print(MC['name'])
    for file_name in MC['file_name_list']:
        file_name = file_name[file_name.rfind("/")+1:]
        #file_name = "ttbar_diLept_madgraph_pythia8_25ns_1"

        a.read_df_from_root(file_name)
        a.save_df_to_csv()

'''Once .csv file is created...'''
#a.read_df_from_csv(file_name)
#a.make_correlation_plot()
#feature_list = ["mct","ptbb"]#,"ngoodjets"
#a.make_scatter_matrix(feature_list)

#import sys
#print('imported')
#if len(sys.argv) < 2:
#    print('Must specify configuration file.')
#    sys.exit(1)
#print(sys.argv[1])