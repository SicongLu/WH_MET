import pandas_analysis
import os
import time
def get_total_file_size(file_list):
    bytes_num = 0
    for file_path in file_list:
        bytes_num += os.path.getsize(file_path)
    return bytes_num

from create_file_list import get_files, getgrid, generate_scan_dict
grid_list = generate_scan_dict()
a = pandas_analysis.pandas_analyzer()
a.set_active_branch()

MC_list = get_files()
read_list = []

#Get the total file size in order to estimate the run time.
total_list = []
for MC in MC_list[:]:#+grid_list[:]:
    total_list += MC["file_name_list"]
total_bytes_num = get_total_file_size(total_list)
print(total_bytes_num*1.0e-6)
print("Total file size to be processed: %.1f Mb"%(total_bytes_num*1.0e-6))
start_time = time.time()
processed_bytes_num = 0

for MC in MC_list[:]:#+grid_list[:]:
    print(MC['name'])
    for file_name in MC['file_name_list']:
        processed_bytes_num += os.path.getsize(file_name)
        file_name = file_name[file_name.rfind("/")+1:]
        #file_name = "ttbar_diLept_madgraph_pythia8_25ns_1"
        read_list.append(file_name)
        #if not("WZTo2L2Q_amcnlo_pythia8_25ns.root" in read_list) or ("WZTo2L2Q" in file_name): continue
        #print(file_name) 
        a.read_df_from_root(file_name)
        a.save_df_to_csv()
    
    current_time = time.time()
    print("Progress: %.1f percent processed"%(processed_bytes_num/total_bytes_num*100.))
    minutes_left = 1.*(current_time-start_time)/processed_bytes_num*(total_bytes_num-processed_bytes_num)/60.
    print("Estimated mintues left: %.1f"%minutes_left)
