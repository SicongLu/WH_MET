import ROOT
import numpy
import array
import math
import time
import multiprocessing as mp
import os
import re
from random import randint
os.nice(15)
ROOT.gStyle.SetOptStat(0);
ROOT.gStyle.SetOptTitle(0);
from palatte_schemes import get_ucsd_palette, get_berkeley_palette
import sys
sys.path.insert(0, '/home/users/siconglu/CMSTAS/software/dataMCplotMaker/')
import dataMCplotMaker
def plot_comparison(var_name, name_list, plot_folder_name, plot_dict):
    hist_list = [hist_dict[MC_name][var_name] for MC_name in name_list]
    #Scale
    
    if_shape_only = True
    if if_shape_only:
        scaled_list = []
        print(var_name)
        for hist in hist_list:
            print(hist.Integral())
            if hist.Integral()!=0:
                hist.Scale(1./hist.Integral())
            scaled_list.append(hist)
        hist_list = scaled_list
        new_opts = {"isLinear": True, "noStack": True,"noFill": True,}
    else:
        new_opts = {"isLinear": False, "noStack": False,"noFill": False,"setMinimum": 1,}
    
    #Remove special chars in var_name:
    tmp_var_name = var_name[:]
    char_str = "!@#$%^&*()[]{};:,./<>?\|`~-=_+"
    char_str = [char_str[i] for i in range(len(char_str))]
    for char in char_str:
        tmp_var_name = tmp_var_name.replace(char,"_")

    if "data" in name_list:
        ind = name_list.index("data")
        h_data = hist_list[ind]
        hist_list = [hist_list[i] for i in range(len(hist_list)) if i != ind]
        name_list = [name_list[i] for i in range(len(name_list)) if i != ind]
    else:
        h_data = ROOT.TH1F("","",1,0,1)
    if "plot_var_name" in plot_dict:
        var_name = plot_dict["plot_var_name"]
    d_opts = {
            "poissonErrorsNoZeros": True,
            "systFillStyle":4050,
            "lumi": 35.9,
            "energy ": 13,
            "outputName": "/home/users/siconglu/CMSTAS/software/niceplots/"+plot_folder_name+tmp_var_name+".pdf",
            "yTitleOffset": -0.12,
            "xAxisLabel": var_name,
            "yAxisLabel": "Events",
            "xAxisUnit": "GeV",
            "noOverflow": True,
            #"legendUp": -0.15,
            #"legendRight": -0.08,
            #"legendTaller": 0.15,
            "outOfFrame": True,
            "type": "Internal",
            "darkColorLines": True,
            "makeTable": True,
            "makeJSON": True,
            }
    d_opts.update(new_opts)
    palette = get_ucsd_palette()
    color_list = [ROOT.TColor.GetColor("#"+palette[item]) for item in palette["default_hist"]]
    dataMCplotMaker.dataMCplot(h_data, bgs=hist_list, titles=name_list, title="", colors=color_list[0:len(name_list)], opts=d_opts)

def get_weight_str(file_name, entry_num, if_dilep = False):
    '''Calculate the relevant weights'''
    #return "1"
    lumi = 35.9
    if "TChiWH" in file_name:
        return "1"
        f_scanSys = ROOT.TFile.Open("/nfs-7/userdata/mliu/tupler_babies/merged/onelepbabymaker/moriond2017.v13/output/SMS_tchiwh.root","READ") 
        h_scanSys = f_scanSys.Get("h_counterSMS").Clone("h_scanSys");
        h_scanN = f_scanSys.Get("histNEvts").Clone("h_scanN"); 
        nums = re.findall(r'\d+', file_name)
        c1mass, n1mass = int(nums[-2]), int(nums[-1])
        
        c1massbin = h_scanN.GetXaxis().FindBin(c1mass);
        n1massbin = h_scanN.GetYaxis().FindBin(n1mass);
        nevents = h_scanN.GetBinContent(c1massbin,n1massbin);
        f_scanSys.Close()
        str_condition = "1*xsec*0.58*0.3*1000*"+str(lumi)+"/"+str(nevents)#Problem on xsec
    elif "data" in file_name:
        return "1"
    else:
        str_condition = "1.0*scale1fb*"+str(lumi)
    str_condition += "*weight_PU*weight_lepSF*weight_btagsf*trigeff"
    return str_condition
    '''
    Use if the triglep is good.
    if if_dilep:
        #trigeff_str = "(1-(1-triglep1)*(1-triglep2))"
        trigeff_str = "(triglep1+triglep2-triglep1*triglep2)"
    else:
        trigeff_str = "triglep1"
    str_condition += "*weight_PU*weight_lepSF*weight_btagsf"+"*"+trigeff_str
    '''
    return str_condition

def get_hists(MC_name, file_name, plot_dict_list):
    print(file_name)
    f = ROOT.TFile(file_name)
    t = f.Get("t")
    weight_str = get_weight_str(file_name, t.GetEntries())
    for plot_dict in plot_dict_list:
        str_condition = plot_dict["str_condition"]
        str_condition = "("+str_condition+")*"+weight_str
        var_name = plot_dict["var_name"]
        xmin, xmax, bin_num = plot_dict["xmin"], plot_dict["xmax"], plot_dict["bin_num"]
        rand_str = str(randint(0, 10000)) 
        myhist = ROOT.TH1F("myhist"+rand_str,"myhist"+rand_str,bin_num,xmin,xmax);
        t.Draw(var_name+">>myhist"+rand_str,str_condition,"goff")
        hist_merge_list.append({"MC_name":MC_name, "var_name":var_name, "hist":myhist})
        continue;
        tmp_dict = hist_dict[MC_name]
        if tmp_dict[var_name] == None:
            tmp_dict[var_name] = myhist
            myhist.SetDirectory(0);
        else:
            tmp_dict[var_name].Add(tmp_dict[var_name], myhist, 1.0, 1.0 )
        hist_dict[MC_name] = tmp_dict
    #ROOT.TH1.AddDirectory(ROOT.kFALSE); 
    
    f.Close()
    return 0  
manager = mp.Manager()
hist_dict = manager.dict()
hist_merge_list  = manager.list()

#Basic Set-up
plot_dict_list = [
{"var_name":"new_mbb",     "plot_var_name":"M_{b#bar{b}}",      "xmin":80, "xmax":180, "bin_num": 20},\
{"var_name":"ngoodjets",   "plot_var_name":"N_{jets}",          "xmin":0, "xmax":10, "bin_num": 10},\
{"var_name":"nbtag_loose", "plot_var_name":"N_{loose b-jets}",  "xmin":0, "xmax":10, "bin_num": 10},\
{"var_name":"nbtag_med",   "plot_var_name":"N_{medium b-jets}", "xmin":0, "xmax":10, "bin_num": 10},\
{"var_name":"ngoodjets30", "plot_var_name":"N_{loose b-jets}",  "xmin":0, "xmax":10, "bin_num": 10},\
{"var_name":"new_mct",     "plot_var_name":"M_{CT}",            "xmin":0, "xmax":800, "bin_num": 20},\
{"var_name":"new_met", "plot_var_name":"E_{T}^{miss}", "xmin":0, "xmax":800, "bin_num": 30},\
{"var_name":"new_mt", "plot_var_name":"m_{T}(#it{l,#nu})", "xmin":10, "xmax":600, "bin_num": 20},\
{"var_name":"MT2W", "xmin":20, "xmax":600, "bin_num": 20},\
{"var_name":"Mlb_closestb", "plot_var_name":"Mlb_{closest b}","xmin":10, "xmax":500, "bin_num": 20},\
{"var_name":"topness", "xmin":-10, "xmax":10, "bin_num": 20},\
{"var_name":"topnessMod", "xmin":-10, "xmax":10, "bin_num": 20},\
{"var_name":"mindphi_met_j1_j2", "plot_var_name":"min#Delta#phi(E_{T}^{miss},j_{1},j_{2})",  "xmin":0, "xmax":5, "bin_num": 20},\
{"var_name":"ak4_htratiom",  "plot_var_name":"H_{T} ratio (Ak4)",  "xmin":0, "xmax":1, "bin_num": 20},\
{"var_name":"ak8GoodPFJets", "plot_var_name":"N_{Ak8 jets}","xmin":0, "xmax":10, "bin_num": 10},\
{"var_name":"ak8pfjets_p4[0].Pt()","plot_var_name":"p_{T, lead Ak8}", "xmin":200, "xmax":1200, "bin_num": 20},\
{"var_name":"ak8pfjets_deep_rawdisc_hbb[0]", "plot_var_name":"Deep flavor Hbb Tag",       "xmin":0, "xmax":1, "bin_num": 20},\
{"var_name":"ak8pfjets_puppi_softdropMass[0]",  "plot_var_name":"mass_{Ak8, puppi softdrop}",      "xmin":0, "xmax":200, "bin_num": 20},\
#
{"var_name":"ak8pfCombinedInclusiveSecondaryVertexV2BJetTags[0]"    , "xmin":0, "xmax":1, "bin_num": 40},\
{"var_name":"ak8pfDeepCSVJetTags_probudsg[0]"                       , "xmin":0, "xmax":1, "bin_num": 40},\
{"var_name":"ak8pfDeepCSVJetTags_probbb[0]"                         , "xmin":0, "xmax":1, "bin_num": 40},\
{"var_name":"ak8pfBoostedDoubleSecondaryVertexAK8BJetTags[0]"       , "plot_var_name":"Lead Ak8 Boosted double-b tag",   "xmin":0, "xmax":1, "bin_num": 40},\
{"var_name":"ak8pfCombinedSecondaryVertexV2BJetTags[0]"             , "xmin":0, "xmax":1, "bin_num": 40},\
{"var_name":"ak8pfCombinedMVAV2BJetTags[0]"                         , "xmin":-1, "xmax":1, "bin_num": 40},\
{"var_name":"ak8pfDeepCSVJetTags_probc[0]"                          , "xmin":0, "xmax":1, "bin_num": 40},\
{"var_name":"ak8pfDeepCSVJetTags_probb[0]"                          , "xmin":0, "xmax":1, "bin_num": 40},\
]
CR_plot_dict_list = [
{"var_name":"ngoodjets",   "plot_var_name":"N_{jets}",          "xmin":0, "xmax":10, "bin_num": 10},\
{"var_name":"new_mct",     "plot_var_name":"M_{CT}",            "xmin":0, "xmax":800, "bin_num": 20},\
{"var_name":"new_met", "plot_var_name":"E_{T}^{miss}", "xmin":0, "xmax":800, "bin_num": 30},\
{"var_name":"new_mt", "plot_var_name":"m_{T}(#it{l,#nu})", "xmin":10, "xmax":600, "bin_num": 20},\
{"var_name":"new_mbb",     "plot_var_name":"M_{b#bar{b}}",      "xmin":80, "xmax":180, "bin_num": 20},\
{"var_name":"lep1_p4.fCoordinates.Pt()",  "plot_var_name":"lead lepton p_{T}","xmin":0, "xmax":500, "bin_num": 25},\
{"var_name":"ak4pfjets_leadbtag_p4.fCoordinates.Pt()", "plot_var_name":"lead b-jet p_{T}","xmin":0, "xmax":500, "bin_num": 25},\
]
#plot_dict_list = CR_plot_dict_list   

#Common set-up 
lumi = 35.9
region_str = "PSR1jet_met_200_pt_300_hbb"
region_str = "PSR1jet_new_met_200_pt_300_hbb"
#region_str = "PSR1jet_met_200_pt_300"
#region_str = "PSR1jet_recover_2jet_met_250_mct220"
#region_str = "PSR1jet_recover_2jet_met_200_mct170"
#region_str = "SR2"
#region_str = "CR2l"
#region_str = "CRMbb_inclusive"
#region_str = "CR0b_inclusive"
#region_str = "CR3j_2l"
#region_str = "CR3j_Mbb_inclusive"
#region_str = "CR3j_0b_inclusive"

plot_folder_name = "WH_Comparison_20180724_v2_"+region_str+"/"

from create_file_list import get_files, get_new_files
MC_list = get_new_files()
#MC_list = get_files()

#new_location = "../root_file_temp/Sicong_20180626/"
#new_location = "../root_file_temp/Sicong_20180716/"
new_location = "../root_file_temp/Sicong_20180722/"

#sample_index_list = [6,7,8,9,10,11]
#sample_index_list = [0,4]#4,1,2,
sample_index_list = [3, 0,  ]#4,1,2,0,
MC_list = [MC_list[index] for index in sample_index_list]
for MC in MC_list:
    MC_name = MC["name"]
    tmp_dict = {}
    for plot_dict in plot_dict_list:
        tmp_dict[plot_dict["var_name"]] = None
    hist_dict[MC_name] = tmp_dict
   
#Cut-Conditions
from selection_criteria import get_cut_dict, combine_cuts
cut_dict, current_cut_list,region_cut_dict = get_cut_dict(if_new_sample = True)
str_condition = region_cut_dict[region_str]

#Change the yield estimate region to plot shapre region definition.
if "0b" in region_str:
    str_condition = str_condition.replace(cut_dict["mt"],"new_mt>50")
elif "Mbb" in region_str:
    str_condition = str_condition.replace(cut_dict["mctbb"],"new_mct>0")
tmp_str_condition = str_condition
#Specify the str_condition for each var_name
for plot_dict in plot_dict_list:
    if "2l" in region_str and not("new_mbb" in plot_dict["var_name"]):
        str_condition = "("+tmp_str_condition+")"+"&&"+cut_dict["m_bb"]
    else:
        str_condition = tmp_str_condition
    plot_dict["str_condition"] = str_condition

#Plotting
num_cores = 40
total_num = len(plot_dict_list)
start_time = time.time()
processes = [] 
name_list = []
index = 0
for MC in MC_list:
    file_name_list = MC["file_name_list"]
    MC_name = MC["name"]
    name_list.append(MC_name) 
    tmp_list = file_name_list[:min(len(file_name_list),100)]
    for file_name in file_name_list:
        tmp_name = file_name
        file_name = new_location + file_name[file_name.rfind("/")+1:]      
        p = mp.Process(target=get_hists, args=(MC_name, file_name, plot_dict_list,))
        processes.append(p)
        index+=1
        if (index)%num_cores == 0 or (tmp_name == file_name_list[-1] and MC == MC_list[-1]):
            [x.start() for x in processes]
            print("Starting %.0f of %.0f process simultaneously."%(len(processes), len(file_name_list)))
            [x.join() for x in processes]
            print("%.0f of %.0f processes have been completed."%(index, len(file_name_list)))
            processes = []
            current_time = time.time()
    
            #Merge
            print("Start merging!!!")
            for tmp_list_dict in hist_merge_list:
                MC_name = tmp_list_dict["MC_name"]
                var_name = tmp_list_dict["var_name"]
                myhist = tmp_list_dict["hist"]
                tmp_dict = hist_dict[MC_name]
                if tmp_dict[var_name] == None:
                    tmp_dict[var_name] = myhist
                    myhist.SetDirectory(0);
                else:
                    tmp_dict[var_name].Add(tmp_dict[var_name], myhist, 1.0, 1.0 )
                hist_dict[MC_name] = tmp_dict
            hist_merge_list[:] = []
processes = []
for plot_dict in plot_dict_list:
    var_name = plot_dict["var_name"]
    plot_comparison(var_name, name_list, plot_folder_name, plot_dict)