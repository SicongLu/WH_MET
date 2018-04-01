import ROOT
import numpy as np
import array
ROOT.gStyle.SetOptStat(0);
ROOT.gStyle.SetOptTitle(0);
import re
def get_used_var(cut_str):
    '''Create the list of sued variables to speed up, using the cut_dict'''
    possible_used_var_list = re.split('+()&|<>*.',cut_str)
    #tmp_var_name = var_name[:]
    return possible_used_var_list
    
    char_str = [char_str[i] for i in range(len(char_str))]
def get_yield(file_name,  region_cut_dict):
    bin_num = 3
    xmin = -1
    xmax = 2
    var_name = "PassTrackVeto"
    lumi = 35.9
    f = ROOT.TFile(file_name)
    t = f.Get("t")
    yield_dict = {}
    stats_dict = {}
    for key, str_condition in region_cut_dict.iteritems():
        if "TChiWH" in file_name:
            str_condition_num = str_condition
            str_condition = "("+str_condition+")*weight_PU*weight_lepSF*weight_btagsf*xsec*0.58*0.3*1000*"+str(lumi)+"/"+str(t.GetEntries())
            str_condition_stats = "("+str_condition+")^2"
        else:
            str_condition_num = str_condition
            str_condition = "("+str_condition+")*scale1fb*"+str(lumi)#*weight_PU*weight_lepSF*weight_btagsf
            str_condition_stats = "("+str_condition+")^2"
        #Evaluate the num    
#        myhist_num_name = "myhist_num"+key
#        myhist_num = ROOT.TH1F(myhist_num_name,myhist_num_name,bin_num,xmin,xmax);
#        t.Draw(var_name+">>"+myhist_num_name,str_condition_num,"goff")
#        resulted_event_num = myhist_num.Integral()
        
        #Evaluate the yield    
        myhist_name = "myhist"+key
        myhist = ROOT.TH1F(myhist_name,myhist_name,bin_num,xmin,xmax);
        t.Draw(var_name+">>"+myhist_name,str_condition,"goff")
        resulted_event_yield = myhist.Integral()
        #Evaluate the statistical uncertainty
        myhist_stats_name = "myhist_stats"+key
        myhist_stats = ROOT.TH1F(myhist_stats_name,myhist_stats_name,bin_num,xmin,xmax);
        t.Draw(var_name+">>"+myhist_stats_name,str_condition_stats,"goff")
        resulted_stats = myhist_stats.Integral()
        
        cut_name = key
        yield_dict[cut_name] = resulted_event_yield
        stats_dict[cut_name] = resulted_stats
        
#        print(resulted_stats, resulted_event_yield*resulted_event_yield/resulted_event_num)
    f.Close()
    return yield_dict, stats_dict

#Basic Set-up
from selection_criteria import get_cut_dict
cut_dict, current_cut_list,region_cut_dict = get_cut_dict()
condition_list = [cut_dict[item] for item in current_cut_list]
print(region_cut_dict.keys())
#Main function
from create_file_list import get_files
MC_list = get_files()
new_location = "../root_file_temp/Sicong_20180327/"

summary_yield_dict = {}
summary_stats_dict = {}
hist_list = []
name_list = []
f_record = open("yield_record.txt","a")
f_record.write("Start Recording...\n")
for MC in MC_list[4:]:#[6:7]:#[10:]:
    MC_name = MC["name"]
    file_name_list = MC["file_name_list"]
    
    sum_dict = {}
    sum_stats_dict = {}
    for file_name in file_name_list:
        file_name = new_location + file_name[file_name.rfind("/")+1:]
        print(file_name)
        f_record.write(file_name+"\n")
        yield_dict, stats_dict = get_yield(file_name,  region_cut_dict)      
        for key, value in yield_dict.iteritems():
            if key in sum_dict.keys():
                sum_dict[key]+=yield_dict[key]
                sum_stats_dict[key]+=stats_dict[key]
            else:
                sum_dict[key]=yield_dict[key]
                sum_stats_dict[key]=stats_dict[key]
        print(sum_dict)
        f_record.write(str(sum_dict)+"\n")
    name_list.append(MC_name)
    summary_yield_dict[MC_name] = sum_dict
    summary_stats_dict[MC_name] = sum_stats_dict
f_record.close()
#Save the yield Table in .csv file
if_transpose = True #Transpose the table to follow the convention
import csv
with open('table_of_yield_03_28.csv', 'w') as csvfile:    #create csv file with w mode
    key_list = [key for key, str_condition in region_cut_dict.iteritems()]
    key_list = sorted(key_list)
    if if_transpose:
        fieldnames = [" "]+key_list
    else:
        fieldnames = [" "]+name_list          #header names
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)    #set the writer
    writer.writeheader()   
    if if_transpose:
        for MC_name in name_list:
            tmp_row = {" ":MC_name}
            for key, str_condition in region_cut_dict.iteritems():          
                #tmp_row[key] = summary_yield_dict[MC_name][key]
                tmp_row[key] = "%.2f +- %.3f"%(summary_yield_dict[MC_name][key],\
                np.sqrt(summary_stats_dict[MC_name][key]))
            writer.writerow(tmp_row)
    else:
        for key, str_condition in region_cut_dict.iteritems():
            tmp_row = {" ":key}
            for MC_name in name_list:
                #tmp_row[MC_name] = summary_yield_dict[MC_name][key]
                tmp_row[key] = "%.2f +- %.3f"%(summary_yield_dict[MC_name][key],\
                np.sqrt(summary_stats_dict[MC_name][key]))
            writer.writerow(tmp_row) 

