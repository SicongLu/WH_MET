import ROOT
import numpy
import array
import math
import time
import multiprocessing as mp
import os
os.nice(19)
ROOT.gStyle.SetOptStat(0);
ROOT.gStyle.SetOptTitle(0);

#def get_weight_str(file_name, entry_num):
#    '''Calculate the relevant weights'''
#    return "weight"
def get_weight_str(file_name, entry_num):
    '''Calculate the relevant weights'''
    #print(c1mass, n1mass, nevents, entry_num)
    return "1"
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
        #str_condition = "1*xsec*0.58*0.3*1000*"+str(lumi)+"/"+str(nevents)
        str_condition = "1*xsec*0.58*0.3*1000*"+str(lumi)+"/"+str(nevents)#Problem on xsec
    else:
        str_condition = "1*scale1fb*"+str(lumi)
    str_condition += "*weight_PU*weight_lepSF*weight_btagsf*trigeff"
    return str_condition

def draw_histo(file_name, var_name, str_condition, bin_num, xmin, xmax):
    #print(file_name, var_name, str_condition, bin_num, xmin, xmax)
    f = ROOT.TFile(file_name)
    t = f.Get("t")
    weight_str = get_weight_str(file_name, t.GetEntries())
    str_condition = "("+str_condition+")*"+weight_str
    myhist = ROOT.TH1F("myhist","myhist",bin_num,xmin,xmax);
    t.Draw(var_name+">>myhist",str_condition,"goff")
    
    #print(myhist.Integral())
    myhist.SetDirectory(0);
    #ROOT.TH1.AddDirectory(ROOT.kFALSE); 
    
    f.Close()
    return myhist
from create_file_list import get_files
def plot_comparison(var_name, xmin, xmax, bin_num, lumi, MC_multi, sample_index_list, plot_folder_name):
    #Remove special chars in var_name:
    tmp_var_name = var_name[:]
    char_str = "!@#$%^&*()[]{};:,./<>?\|`~-=_+"
    char_str = [char_str[i] for i in range(len(char_str))]
    for char in char_str:
        tmp_var_name = tmp_var_name.replace(char,"_")
    #Collect histograms
    MC_list = get_files()
    hist_list = []
    name_list = []
    new_location = "../root_file_temp/Sicong_20180408/"
    #new_location = "../root_file_temp/XGB_20180410/"
    for MC in [MC_list[index] for index in sample_index_list]:
        MC_name = MC["name"]
        file_name_list = MC["file_name_list"]
        if not("(" in MC_name) and "genbosons_id==25" in var_name:
            continue
        sum_hist = ROOT.TH1F("sum_hist"+tmp_var_name+str(len(name_list)),"sum_hist",bin_num,xmin,xmax)
        #sum_hist.SetDirectory(0);  
        #ROOT.TH1.AddDirectory(ROOT.kFALSE);
        sum_dict = {}
        for file_name in file_name_list:
            file_name = new_location + file_name[file_name.rfind("/")+1:]
            #print(file_name)
            hist = draw_histo(file_name, var_name, str_condition, bin_num, xmin, xmax)
            sum_hist.Add( sum_hist, hist, 1.0, 1.0 )
         
        hist_list.append(sum_hist)
        name_list.append(MC_name)
    for MC in [MC_list[index] for index in sample_index_list]:
        MC_name = MC["name"]
        if "(" in MC_name and "2l top" in name_list:
            index = name_list.index(MC_name)
            if (hist_list[index].Integral() == 0):
                continue;
            MC_multi = math.ceil(1.0*hist_list[name_list.index("2l top")].Integral()/hist_list[index].Integral())
            hist_list[index].Scale(MC_multi)
            name_list[index] += " x " + str(MC_multi)        
    import sys
    sys.path.insert(0, '/home/users/siconglu/CMSTAS/software/dataMCplotMaker/')
    import dataMCplotMaker

    h_data = ROOT.TH1F("","",1,0,1)
    d_opts = {
            "poissonErrorsNoZeros": True,"systFillStyle":4050,
            "lumi": 35.9,
            "energy ": 13,
            "outputName": "/home/users/siconglu/CMSTAS/software/niceplots/"+plot_folder_name+tmp_var_name+".pdf",
            "yTitleOffset": -0.,
            "xAxisLabel": var_name,
            "yAxisLabel": "Events",
            "xAxisUnit": "GeV",
            "noFill": False,
            "isLinear": False,
            #"noStack": False,
            #"noOverflow": True,
            #"legendUp": -0.15,
            #"legendRight": -0.08,
            #"legendTaller": 0.15,
            "outOfFrame": True,
            "type": "Internal",
            #"noGrass": True,
            "darkColorLines": True,
            "makeTable": True,
            "makeJSON": True,
            #"flagLocation": "0.5,0.7,0.15", # add a US flag because 'merica
            }
    color_list = [ROOT.kOrange, ROOT.kSpring, ROOT.kTeal,ROOT.kAzure, ROOT.kViolet, ROOT.kPink, ROOT.kBlack]
    dataMCplotMaker.dataMCplot(h_data, bgs=hist_list, titles=name_list, title="", colors=color_list[0:len(name_list)], opts=d_opts)
    

#Basic Set-up
#Other relevant set-up
plot_dict_list = [#{"var_name":"ptbb", "xmin":20, "xmax":600, "bin_num": 40},\
#{"var_name":"ngoodjets", "xmin":0, "xmax":10, "bin_num": 10},\
##{"var_name":"genbosons_id", "xmin":15, "xmax":30, "bin_num": 15},\
##{"var_name":"genbosons_p4.fCoordinates.M()", "xmin":50, "xmax":150, "bin_num": 25},\
##{"var_name":"genbosons_p4.fCoordinates.M()*(genbosons_id==25)", "xmin":50, "xmax":150, "bin_num": 25},\
#{"var_name":"genbosons_p4.fCoordinates.Pt()*(genbosons_id==25)", "xmin":25, "xmax":1000, "bin_num": 25},\
##{"var_name":"ak4pfjets_p4[0].fCoordinates.Pt()", "xmin":25, "xmax":1000, "bin_num": 25},\
##{"var_name":"genqs_p4[0].fCoordinates.Pt()", "xmin":1, "xmax":1000, "bin_num": 25},\
##{"var_name":"genqs_p4[1].fCoordinates.Pt()", "xmin":1, "xmax":1000, "bin_num": 25},\
##{"var_name":"genqs_p4[2].fCoordinates.Pt()", "xmin":1, "xmax":1000, "bin_num": 25},\
{"var_name":"new_mct", "xmin":0, "xmax":500, "bin_num": 25},\
{"var_name":"new_met", "xmin":0, "xmax":500, "bin_num": 25},\
{"var_name":"new_mt", "xmin":0, "xmax":500, "bin_num": 25},\
{"var_name":"new_mbb", "xmin":0, "xmax":500, "bin_num": 25},\
#{"var_name":"MT2W", "xmin":20, "xmax":600, "bin_num": 20},\
#{"var_name":"Mlb_closestb", "xmin":10, "xmax":500, "bin_num": 20},\
#{"var_name":"topness", "xmin":-10, "xmax":10, "bin_num": 20},\
#{"var_name":"topnessMod", "xmin":-10, "xmax":10, "bin_num": 20},\
#{"var_name":"mindphi_met_j1_j2", "xmin":0, "xmax":5, "bin_num": 20},\
##{"var_name":"mbb*(ptbb>500)", "xmin":50, "xmax":200, "bin_num": 20},\
#{"var_name":"ak4_htratiom", "xmin":0, "xmax":1, "bin_num": 20},\
#
{"var_name":"lep1_p4.fCoordinates.Pt()", "xmin":0, "xmax":500, "bin_num": 25},\
{"var_name":"ak4pfjets_leadbtag_p4.fCoordinates.Pt()", "xmin":0, "xmax":500, "bin_num": 25},\
#{"var_name":"ak4pfjets_p4.fCoordinates.Pt()*(ak4pfjets_CSV > 0.5426)", "xmin":10, "xmax":200, "bin_num": 20},\
#{"var_name":"xgb_proba", "xmin":0, "xmax":1, "bin_num": 40},\
]


#Common set-up 
lumi = 35.9
#plot_folder_name = "WH_Comparison_20180321_alljets/"
#plot_folder_name = "WH_Comparison_20180315_1jet/"
#plot_folder_name = "WH_Comparison_20180315_2jet/"

#region_str = "SR2"
#region_str = "xgb0p7"
#region_str = "PSR3jet_met_200_mct250"
#region_str = "PSR3jet_met_200_mct225"
region_str = "CR2l"
#region_str = "CRMbb_inclusive"
#region_str = "CR0b_inclusive"
plot_folder_name = "WH_CR_Distribution_20180425"+region_str+"/"

sample_index_list = [6,7,8,9,10]
MC_multi = 10
#Cut-Conditions
from selection_criteria import get_cut_dict, combine_cuts
cut_dict, current_cut_list,region_cut_dict = get_cut_dict()
#Current Ordering of the cut-requirement: (Preselection)
#current_cut_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
#"PassTauVeto", "ngoodjets","goodbtags", "m_bb", "event_met_pt", "mt"]
#current_cut_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
#"PassTauVeto", "event_met_pt", "mt"]

#current_condition_list = [cut_dict[item] for item in current_cut_list]
#str_condition = combine_cuts(current_condition_list)
#str_condition +="&& ngoodjets == 1"
#str_condition +="&& ngoodjets == 2"
str_condition = region_cut_dict[region_str]
if "CR0b" in region_str:
    str_condition = str_condition.replace(cut_dict["mt"],"new_mt>50")
elif "CRMbb" in region_str:
    str_condition = str_condition.replace(cut_dict["mctbb"],"new_mct>0")
elif "CR2l" in region_str:
    str_condition = str_condition.replace(cut_dict["event_met_pt_high"],cut_dict["event_met_pt"])
print(str_condition)
#Plotting
num_cores = 12
total_num = len(plot_dict_list)
start_time = time.time()
processes = []
for plot_dict in plot_dict_list:
    print(plot_dict)
    index = plot_dict_list.index(plot_dict)
    #plot_comparison(plot_dict["var_name"], plot_dict["xmin"], plot_dict["xmax"], plot_dict["bin_num"], lumi, MC_multi, sample_index_list, plot_folder_name)
    p = mp.Process(target=plot_comparison, args=(plot_dict["var_name"], plot_dict["xmin"], plot_dict["xmax"], plot_dict["bin_num"], lumi, MC_multi, sample_index_list, plot_folder_name,))
    processes.append(p)
    if (index+1)%num_cores == 0 or index+1 == total_num:            
        [x.start() for x in processes]
        print("Starting %.0f process simultaneously."%len(processes))
        [x.join() for x in processes]
        print("%.0f processes have been completed."%len(processes))
        current_time = time.time()
        print("Processing %.0f of %.0f"%(index+1, total_num))
        print("Expect to complete in %.2f miniutes"%(1.*(current_time-start_time)/index*(total_num-index-1)/60.))
        processes = []


