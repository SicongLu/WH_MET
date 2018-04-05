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
a.load_xgb_model()
read_list = []
MC_list = get_files()
for MC in MC_list[0:6]:
    print(MC['name'])
    for file_name in MC['file_name_list']:
        file_name = file_name[file_name.rfind("/")+1:]
        file_name = file_name[:file_name.rfind(".")]
        read_list.append(file_name)
        #if not ("WZTo2L2Q_amcnlo_pythia8_25ns" in read_list) or "WZTo2L2Q_amcnlo_pythia8_25ns" == file_name: continue
        #a.read_df_from_root(file_name)
        a.load_csv(file_name)
        a.apply_xgb_proba()
        #a.save_df_to_csv()
        a.save_df_to_root()

        

'''Once .csv file is created...'''
#a.read_df_from_csv(file_name)
#a.make_correlation_plot()
#feature_list = ["mct","ptbb"]#,"ngoodjets"
#a.make_scatter_matrix(feature_list)
'''Get input if needed.'''
#import sys
#print('imported')
#if len(sys.argv) < 2:
#    print('Must specify configuration file.')
#    sys.exit(1)
#print(sys.argv[1])