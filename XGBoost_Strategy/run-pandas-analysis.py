'''
This is the main script for relevant pandas analysis, including:
Reading the datafrom from both .csv and .root;
Generate relevant feature;
Skim to only relevant feature;
Make correlation of features;
Use xGBoost to explore the limit of our analysis; (not for actual analysis);
'''

import pandas_analysis
import os
import time
def get_total_file_size(file_list):
    bytes_num = 0
    for file_path in file_list:
        bytes_num += os.path.getsize(file_path)
    return bytes_num


from create_file_list import get_files, getgrid, generate_scan_dict
a = pandas_analysis.pandas_analyzer()
a.set_active_branch()
a.load_xgb_model("xgb_model_0412.xgb")
read_list = []
MC_list = get_files()
#for MC in MC_list[0:6]:
grid_list = generate_scan_dict()

#Get the total file size in order to estimate the run time.
total_list = []
for MC in grid_list[0:0]+MC_list[6:]:
    total_list += MC["file_name_list"]
total_bytes_num = get_total_file_size(total_list)
print(total_bytes_num*1.0e-6)
print("Total file size to be processed: %.1f Mb"%(total_bytes_num*1.0e-6))
start_time = time.time()
processed_bytes_num = 0
name_list = []
for MC in grid_list[0:0]+MC_list[6:]:
    print(MC['name'])
    for file_name in MC['file_name_list']:
        processed_bytes_num += os.path.getsize(file_name)
        file_name = file_name[file_name.rfind("/")+1:]
        file_name = file_name[:file_name.rfind(".")]
        read_list.append(file_name)
        
#
#        a.load_csv(file_name)
#        a.apply_xgb_proba()
#        #a.save_df_to_csv()
#        a.save_df_to_root()
#
#        current_time = time.time()
#        print("Progress: %.1f percent processed"%(processed_bytes_num/total_bytes_num*100.))
#        minutes_left = 1.*(current_time-start_time)/processed_bytes_num*(total_bytes_num-processed_bytes_num)/60.
#        print("Estimated mintues left: %.1f"%minutes_left)
a.multiprocessing(read_list, 5)
        

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