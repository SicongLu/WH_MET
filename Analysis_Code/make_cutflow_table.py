import ROOT
import numpy
import array
ROOT.gStyle.SetOptStat(0);
ROOT.gStyle.SetOptTitle(0);

def get_cutflow(file_name,  condition_list):
    '''Return the cutflow dictionary for 1 MC file.'''
    bin_num = 3
    xmin = -1
    xmax = 2
    var_name = "PassTrackVeto"
    lumi = 35.9
    f = ROOT.TFile(file_name)
    t = f.Get("t")
    cutflow_dict = {}
    for i in range(len(condition_list) + 1):
        str_condition = "1"
        for j in range(i):
            str_condition += "&&"
            str_condition += condition_list[j]
        str_condition = "("+str_condition+")*weight"
        myhist_name = "myhist"+str(i)
        myhist = ROOT.TH1F(myhist_name,myhist_name,bin_num,xmin,xmax);
        t.Draw(var_name+">>"+myhist_name,str_condition,"goff")
        resulted_event_num = myhist.Integral()
        if i == 0:  cut_name = "no cut"
        else:  cut_name = condition_list[i-1]
        cutflow_dict[cut_name] = resulted_event_num
    from collections import OrderedDict
    cutflow_dict = OrderedDict(sorted(cutflow_dict.items(), key=lambda x: x[1], reverse=True)) 
    
    f.Close()
    return cutflow_dict

def get_summary_cutflow(condition_list, new_location, MC_list):
    '''Return the summary cutflow dictionary with full MC.'''
    summary_cutflow_dict = {}
    hist_list = []
    name_list = []
    for MC in MC_list:
        MC_name = MC["name"]
        file_name_list = MC["file_name_list"]
        
        sum_dict = {}
        for file_name in file_name_list:
            file_name = new_location + file_name[file_name.rfind("/")+1:]
            print(file_name)
            cutflow_dict = get_cutflow(file_name,  condition_list)      
            for key, value in cutflow_dict.items():
                if key in sum_dict.keys():
                    sum_dict[key]+=cutflow_dict[key]
                else:
                    sum_dict[key]=cutflow_dict[key] 
        name_list.append(MC_name)
        summary_cutflow_dict[MC_name] = sum_dict
    return summary_cutflow_dict, name_list

def get_n_minus_1(condition_list, new_location, MC_list):
    '''Return the summary cutflow dictionary with full MC.'''
    n_minus_1_dict = {}
    hist_list = []
    name_list = []
    for MC in MC_list:
        MC_name = MC["name"]
        file_name_list = MC["file_name_list"]
        
        sum_dict = {}
        for file_name in file_name_list:
            file_name = new_location + file_name[file_name.rfind("/")+1:]
            print(file_name)
            cutflow_dict = {}
            for key in condition_list+["all cut"]:
                str_condition = "1"
                for condition in condition_list:
                    if condition == key: continue
                    str_condition += "&&"
                    str_condition += condition
                tmp_cutflow_dict = get_cutflow(file_name, [str_condition])
                tmp_cutflow_dict[key] = tmp_cutflow_dict.pop(str_condition)
                cutflow_dict.update(tmp_cutflow_dict)                
            for key, value in cutflow_dict.items():
                if key in sum_dict.keys():
                    sum_dict[key]+=cutflow_dict[key]
                else:
                    sum_dict[key]=cutflow_dict[key] 
        name_list.append(MC_name)
        n_minus_1_dict[MC_name] = sum_dict
    return n_minus_1_dict, name_list
import csv
def write_cutflow(summary_cutflow_dict, condition_list, name_list, name_str = ""):
    '''Save the cutflow.'''
    #Save the Cutflow Table in .csv file
    with open('cutflow_table_'+name_str+'.csv', 'w') as csvfile:    #create csv file with w mode
        fieldnames = [" "]+name_list          #header names
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)    #set the writer
        writer.writeheader()  
        for key in ["no cut"]+condition_list:
            if key == "no cut" and "n_minus_1" in name_str:
                key = "all cut"
            tmp_row = {" ":key}
            for MC_name in name_list:
                tmp_row[MC_name] = summary_cutflow_dict[MC_name][key]
            writer.writerow(tmp_row) 
    #Add Efficiency
    with open('cutflow_efficiency_'+name_str+'.csv', 'w') as csvfile:    #create csv file with w mode
        fieldnames = [" "]+name_list          #header names
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)    #set the writer
        writer.writeheader()
        full_condition_list = ["no cut"]+condition_list 
        for key in condition_list:
            tmp_row = {" ":key}
            for MC_name in name_list:
                previous_key = full_condition_list[full_condition_list.index(key)-1]
                if "n_minus_1" in name_str:
                    tmp_row[MC_name] = "%.2f"%(1.*summary_cutflow_dict[MC_name][key]/summary_cutflow_dict[MC_name]["all cut"]*100.)
                else:
                    tmp_row[MC_name] = "%.2f"%(1.*summary_cutflow_dict[MC_name][key]/summary_cutflow_dict[MC_name][previous_key]*100.)
            writer.writerow(tmp_row)
        if "n_minus_1" in name_str: return;
        last_key = condition_list[-1]
        for MC_name in name_list:
            tmp_row[MC_name] = "%.4f"%(1.*summary_cutflow_dict[MC_name][last_key]/summary_cutflow_dict[MC_name]["no cut"]*100.)
        writer.writerow(tmp_row)

#Basic Set-up
from selection_criteria import get_cut_dict
cut_dict, current_cut_list,region_cut_dict = get_cut_dict()
condition_list = [cut_dict[item] for item in current_cut_list]
print(condition_list)
#Main function
from create_file_list import get_files, getgrid, generate_scan_dict
grid_list = generate_scan_dict()
MC_list = get_files()
new_location = "../root_file_temp/XGB_20180410/"
summary_cutflow_dict, name_list = get_summary_cutflow(condition_list, new_location, MC_list[0:6])#[0:6]
date = "0412"
write_cutflow(summary_cutflow_dict, condition_list, name_list, name_str = date)

n_minus_1_dict, name_list = get_n_minus_1(condition_list, new_location, MC_list[0:6])
date = "n_minus_1_0412"
write_cutflow(n_minus_1_dict, condition_list, name_list, name_str = date)




