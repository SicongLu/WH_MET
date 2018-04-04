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
def getgrid():
    grid = [[150, 1], [150, 24], \
    [175, 1], [175, 25], [175, 49], \
    [200, 1], [200, 25], [200, 50], [200, 74], \
    [225, 1], [225, 25], [225, 50], [225, 75], [225, 99], \
    [250, 1], [250, 25], [250, 50], [250, 75], [250, 100], [250, 124], \
    [275, 1], [275, 25], [275, 50], [275, 75], [275, 100], [275, 125], [275, 149], \
    [300, 1], [300, 25], [300, 50], [300, 75], [300, 100], [300, 125], [300, 150], [300, 174], \
    [325, 1], [325, 25], [325, 50], [325, 75], [325, 100], [325, 125], [325, 150], [325, 175], [325, 199], \
    [350, 1], [350, 25], [350, 50], [350, 75], [350, 100], [350, 125], [350, 150], [350, 175], [350, 200], [350, 224], \
    [375, 1], [375, 25], [375, 50], [375, 75], [375, 100], [375, 125], [375, 150], [375, 175], [375, 200], [375, 225], [375, 249], \
    [400, 1], [400, 25], [400, 50], [400, 75], [400, 100], [400, 125], [400, 150], [400, 175], [400, 200], [400, 225], [400, 250], [400, 274], \
    [425, 1], [425, 25], [425, 50], [425, 75], [425, 100], [425, 125], [425, 150], [425, 175], [425, 200], [425, 225], [425, 250], [425, 275], [425, 299], \
    [450, 1], [450, 25], [450, 50], [450, 75], [450, 100], [450, 125], [450, 150], [450, 175], [450, 200], [450, 225], [450, 250], [450, 275], [450, 300], \
    [475, 1], [475, 25], [475, 50], [475, 75], [475, 100], [475, 125], [475, 150], [475, 175], [475, 200], [475, 225], [475, 250], [475, 275], [475, 300], \
    [500, 1], [500, 25], [500, 50], [500, 75], [500, 100], [500, 125], [500, 150], [500, 175], [500, 200], [500, 225], [500, 250], [500, 275], [500, 300], \
    [525, 1], [525, 25], [525, 50], [525, 75], [525, 100], [525, 125], [525, 150], [525, 175], [525, 200], [525, 225], [525, 250], [525, 275], [525, 300], \
    [550, 1], [550, 25], [550, 50], [550, 75], [550, 100], [550, 125], [550, 150], [550, 175], [550, 200], [550, 225], [550, 250], [550, 275], [550, 300], \
    [575, 1], [575, 25], [575, 50], [575, 75], [575, 100], [575, 125], [575, 150], [575, 175], [575, 200], [575, 225], [575, 250], [575, 275], [575, 300], \
    [600, 1], [600, 25], [600, 50], [600, 75], [600, 100], [600, 125], [600, 150], [600, 175], [600, 200], [600, 225], [600, 250], [600, 275], [600, 300], \
    [625, 1], [625, 25], [625, 50], [625, 75], [625, 100], [625, 125], [625, 150], [625, 175], [625, 200], [625, 225], [625, 250], [625, 275], [625, 300], \
    [650, 1], [650, 25], [650, 50], [650, 75], [650, 100], [650, 125], [650, 150], [650, 175], [650, 200], [650, 225], [650, 250], [650, 275], [650, 300], \
    [675, 1], [675, 25], [675, 50], [675, 75], [675, 100], [675, 125], [675, 150], [675, 175], [675, 200], [675, 225], [675, 250], [675, 275], [675, 300], \
    [700, 1], [700, 25], [700, 50], [700, 75], [700, 100], [700, 125], [700, 150], [700, 175], [700, 200], [700, 225], [700, 250], [700, 275], [700, 300], \
    [126, 1]]
    # need to printout a card called cards/points_TChiWH.txt
#    points = open('cards/points_tchwh.txt','w') 
#    for point in grid:
#        points.write(str('tchwh_'+str(point[0])+'_'+str(point[1]))+'\n')
    return grid
def generate_scan_dict():
    grid = getgrid()
    grid_list = []
    for point in grid:
        tmp_dict = {}
        tmp_dict["name"] = "(%.0f, %.0f)"%(point[0], point[1])
        tmp_dict["file_name_list"] = ["TChiWH_%.0f_%.0f.root)"%(point[0], point[1])]
        
    return grid_list
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
new_location = "../root_file_temp/Grid_20180404/"
for MC in grid_list[0:4]:
    MC_name = MC["name"]
    file_name = MC["file_name_list"][0]
    yield_dict, stats_dict = get_yield(file_name,  region_cut_dict)
    f_record.write(str(yield_dict)+"\n")
    name_list.append(MC_name)
    summary_yield_dict[MC_name] = yield_dict
    summary_stats_dict[MC_name] = stats_dict
    
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

