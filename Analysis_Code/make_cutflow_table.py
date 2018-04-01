import ROOT
import numpy
import array
ROOT.gStyle.SetOptStat(0);
ROOT.gStyle.SetOptTitle(0);

def get_cutflow(file_name,  condition_list):
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
        if "TChiWH" in file_name:
            str_condition = "("+str_condition+")*weight_PU*weight_lepSF*weight_btagsf*xsec*0.58*0.3*1000*"+str(lumi)+"/"+str(t.GetEntries())
        else:
            str_condition = "("+str_condition+")*weight_PU*weight_lepSF*weight_btagsf*scale1fb*"+str(lumi)
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

#Basic Set-up
from selection_criteria import get_cut_dict
cut_dict, current_cut_list,region_cut_dict = get_cut_dict()
condition_list = [cut_dict[item] for item in current_cut_list]
print(condition_list)
#Main function
from create_file_list import get_files
MC_list = get_files()
new_location = "../root_file_temp/Sicong_20180228/"

summary_cutflow_dict = {}
hist_list = []
name_list = []
for MC in MC_list[0:6]:
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

#Save the Cutflow Table in .csv file
import csv
with open('cutflow_table.csv', 'w') as csvfile:    #create csv file with w mode
    fieldnames = [" "]+name_list          #header names
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)    #set the writer
    writer.writeheader()   
    for key in ["no cut"]+condition_list:
        tmp_row = {" ":key}
        for MC_name in name_list:
            tmp_row[MC_name] = summary_cutflow_dict[MC_name][key]
        writer.writerow(tmp_row) 

