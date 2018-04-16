from create_file_list import get_files, getgrid, generate_scan_dict
import ROOT
import numpy as np
import array
import re
ROOT.gStyle.SetOptStat(0);
ROOT.gStyle.SetOptTitle(0);
import re
def get_used_var(cut_str):
    '''Create the list of sued variables to speed up, using the cut_dict'''
    possible_used_var_list = re.split('+()&|<>*.',cut_str)
    #tmp_var_name = var_name[:]
    return possible_used_var_list
    
    char_str = [char_str[i] for i in range(len(char_str))]

def get_weight_str(file_name, entry_num):
    '''Calculate the relevant weights'''
    #print(c1mass, n1mass, nevents, entry_num)
    lumi = 35.9
    if "TChiWH" in file_name:
        f_scanSys = ROOT.TFile.Open("/nfs-7/userdata/mliu/tupler_babies/merged/onelepbabymaker/moriond2017.v13/output/SMS_tchiwh.root","READ") 
        h_scanSys = f_scanSys.Get("h_counterSMS").Clone("h_scanSys");
        h_scanN = f_scanSys.Get("histNEvts").Clone("h_scanN"); 
        nums = re.findall(r'\d+', file_name)
        c1mass, n1mass = int(nums[-2]), int(nums[-1])
        
        c1massbin = h_scanN.GetXaxis().FindBin(c1mass);
        n1massbin = h_scanN.GetYaxis().FindBin(n1mass);
        nevents = h_scanN.GetBinContent(c1massbin,n1massbin);
        f_scanSys.Close()
        str_condition = "1*xsec*0.58*0.3*1000*"+str(lumi)+"/"+str(nevents)
    else:
        str_condition = "1*scale1fb*"+str(lumi)
    str_condition += "*weight_PU*weight_lepSF*weight_btagsf*trigeff"
    
    return str_condition    
def get_yield(file_name,  region_cut_dict):
    bin_num = 3
    xmin = -1
    xmax = 2
    var_name = "PassTrackVeto"

#    bin_num = 2
#    xmin = -2
#    xmax = 100
#    var_name = "ngoodjets"
    lumi = 35.9
    f = ROOT.TFile(file_name)
    t = f.Get("t")
    yield_dict = {}
    stats_dict = {}
    for key, str_condition in region_cut_dict.iteritems():
        str_condition_num = str_condition
        #weight_str = "(weight)"
        weight_str = "("+get_weight_str(file_name, t.GetEntries())+")"
        str_condition = "("+str_condition+")*"+weight_str
        str_condition_stats = str_condition+"^2"
#        #Evaluate the num    
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
##Select those with xgb criteria
new_dict = {}
for key, item in region_cut_dict.iteritems():
    if  ("4jet" in key):
        new_dict[key] = item
region_cut_dict = new_dict
#Main function
MC_list = get_files()
grid_list = generate_scan_dict()

summary_yield_dict = {}
summary_stats_dict = {}
hist_list = []
name_list = []
f_record = open("yield_record.txt","a")
f_record.write("Start Recording...\n")

import os
import time
def get_total_file_size(file_list):
    bytes_num = 0
    for file_path in file_list:
        bytes_num += os.path.getsize(file_path)
    return bytes_num
#Get the total file size in order to estimate the run time.
total_list = []
for MC in grid_list[:]+MC_list[6:]:
    total_list += MC["file_name_list"]
total_bytes_num = get_total_file_size(total_list)
print(total_bytes_num*1.0e-6)
print("Total file size to be processed: %.1f Mb"%(total_bytes_num*1.0e-6))
start_time = time.time()
processed_bytes_num = 0

new_location = "../root_file_temp/XGB_20180410/" #Skimmed Codes
for MC in grid_list[:]:
    MC_name = MC["name"]
    print(MC_name)
    file_name = MC["file_name_list"][0]
    processed_bytes_num += os.path.getsize(file_name)
    file_name = new_location + file_name[file_name.rfind("/")+1:]
    yield_dict, stats_dict = get_yield(file_name,  region_cut_dict)
    f_record.write(str(yield_dict)+"\n")
    name_list.append(MC_name)
    summary_yield_dict[MC_name] = yield_dict
    summary_stats_dict[MC_name] = stats_dict
    print(yield_dict)
    print(stats_dict)
    current_time = time.time()
    print("Progress: %.1f percent processed"%(processed_bytes_num/total_bytes_num*100.))
    minutes_left = 1.*(current_time-start_time)/processed_bytes_num*(total_bytes_num-processed_bytes_num)/60.
    print("Estimated mintues left: %.1f"%minutes_left)
for MC in MC_list[6:]:
    MC_name = MC["name"]
    file_name_list = MC["file_name_list"]
    
    sum_dict = {}
    sum_stats_dict = {}
    for file_name in file_name_list:
        processed_bytes_num += os.path.getsize(file_name)
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
        current_time = time.time()
        print("Progress: %.1f percent processed"%(processed_bytes_num/total_bytes_num*100.))
        minutes_left = 1.*(current_time-start_time)/processed_bytes_num*(total_bytes_num-processed_bytes_num)/60.
        print("Estimated mintues left: %.1f"%minutes_left)
    name_list.append(MC_name)
    summary_yield_dict[MC_name] = sum_dict
    summary_stats_dict[MC_name] = sum_stats_dict
f_record.close()
#Save the yield Table in .csv file
if_transpose = True #Transpose the table to follow the convention
import csv
with open('table_of_yield_04_12_sub_4jets.csv', 'w') as csvfile:    #create csv file with w mode
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

