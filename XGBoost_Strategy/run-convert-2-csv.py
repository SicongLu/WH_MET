import pandas_analysis
from create_file_list import get_files, getgrid, generate_scan_dict
a = pandas_analysis.pandas_analyzer()
a.set_active_branch()

MC_list = get_files()
read_list = []

grid_list = generate_scan_dict()
for MC in MC_list[0:6]:#+grid_list[0:1]
    print(MC['name'])
    for file_name in MC['file_name_list']:
        file_name = file_name[file_name.rfind("/")+1:]
        #file_name = "ttbar_diLept_madgraph_pythia8_25ns_1"
        read_list.append(file_name)
        if not("WZTo2L2Q_amcnlo_pythia8_25ns.root" in read_list) or ("WZTo2L2Q" in file_name): continue
        print(file_name) 
        a.read_df_from_root(file_name)
        a.save_df_to_csv()
