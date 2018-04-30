import ROOT
import numpy
import array
import math
ROOT.gStyle.SetOptStat(0);
ROOT.gStyle.SetOptTitle(0);
def delta_R(v1, v2):
    dphi = abs(v1.Phi()-v2.Phi())
    if dphi>math.pi: dphi = 2*math.pi - dphi
    deta = abs(v1.Eta()-v2.Eta())
    dR = numpy.sqrt(dphi*dphi+deta*deta)
    return dR
def draw_histo(file_name, str_condition):
    #print(file_name, var_name, str_condition, bin_num, xmin, xmax)
    f = ROOT.TFile(file_name)
    t = f.Get("t")
    var_name = "dR_bb"
    bin_num = 40
    xmin = 0
    xmax = 3.5
    myhist1 = ROOT.TH1F("myhist1","myhist1",bin_num,xmin,xmax);
    myhist2 = ROOT.TH1F("myhist2","myhist2",bin_num,xmin,xmax);
    str_condition +="&& ngoodjets == 2"
    weight_form = ROOT.TTreeFormula("weight",str_condition,t)
    for i in range(t.GetEntries()):
        if i % 1e4 == 0: print(i)
        #if i>10000: break;
        t.GetEntry(i)
        dR_bb = -999
        weight = weight_form.EvalInstance()
        if weight == 0:
            continue
        #Calculate dR_bb
        m_id = t.genqs_motherid
        v1 = 0
        v2 = 0
        for i in range(len(m_id)):
            if t.genqs_motherid.at(i) == 25 and t.genqs_id.at(i) == -5 and v1 == 0:
                v1 = t.genqs_p4.at(i)
            if t.genqs_motherid.at(i) == 25 and t.genqs_id.at(i) == 5 and v2 == 0:
                v2 = t.genqs_p4.at(i)        
        dR_bb = delta_R(v1,v2)
        #Genenrator info.
        
        p4_list = t.ak4pfjets_p4
        pT_list = [p4.Pt() for p4 in p4_list] 
        pT_list = sorted(pT_list, reverse=True)
        #If it is in 1 jet region
        value = dR_bb
        if len(pT_list) == 1 and pT_list[0]>=30: #1 jet region
            myhist1.Fill(value, weight)
        elif len(pT_list) >= 2 and pT_list[0]>=30 and pT_list[1]<30:
            myhist1.Fill(value, weight)
        elif len(pT_list) == 2 and pT_list[1]>=30: #2 jet region
            myhist2.Fill(value, weight)
        elif len(pT_list) > 2 and pT_list[1]>=30 and pT_list[2]<30:
            myhist2.Fill(value, weight)
        
    myhist1.SetDirectory(0);
    myhist2.SetDirectory(0); 
    
    f.Close()
    return myhist1, myhist2
from create_file_list import get_files
def flatten_var_name(var_name):
    #Remove special chars in var_name:
    tmp_var_name = var_name[:]
    char_str = "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "
    char_str = [char_str[i] for i in range(len(char_str))]
    for char in char_str:
        tmp_var_name = tmp_var_name.replace(char,"_")
    return tmp_var_name
def plot_comparison(MC, plot_folder_name, var_name = "dR_bb"):
    #Remove special chars in var_name:
        
    #Collect histograms
    MC_list = get_files()
    new_location = "../root_file_temp/Sicong_20180422/"
    
    MC_name = MC["name"]
    tmp_var_name = flatten_var_name(MC_name+"_dR_bb")
    file_name_list = MC["file_name_list"]
    file_name = file_name_list[0]
    file_name = new_location + file_name[file_name.rfind("/")+1:]
    hist1, hist2 = draw_histo(file_name, str_condition)
    hist_list = [hist1, hist2]
    name_list = [MC_name+"1 jet", MC_name+"2 jet"]
        
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
            "noFill": True,
            "isLinear": True,
            "noOverflow": True,
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
plot_dict_list = [
{"var_name":"ak4pf_separate_high", "xmin":0, "xmax":50, "bin_num": 25},\
{"var_name":"ak4pf_separate_low", "xmin":0, "xmax":50, "bin_num": 25},\
]

#Common set-up 
lumi = 35.9

plot_folder_name = "WH_Comparison_20180422_compare_1jet_2jet/"
sample_index_list = [2, 3, 4, 5]
MC_multi = 300

#Cut-Conditions
from selection_criteria import get_cut_dict, combine_cuts
cut_dict, current_cut_list,region_cut_dict = get_cut_dict()
#Current Ordering of the cut-requirement: (Preselection)
#current_cut_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
#"PassTauVeto", "ngoodjets","goodbtags", "m_bb", "event_met_pt", "mt"]
current_cut_list = ["passTrigger", "passOneLep", "passLepSel", "PassTrackVeto",\
"PassTauVeto", "event_met_pt", "mt"]

current_condition_list = [cut_dict[item] for item in current_cut_list]
str_condition = combine_cuts(current_condition_list)
#Plotting
plot_dict = plot_dict_list[0]
tmp_MC_list = [
{"name":"new (700,1)", "file_name_list":["/home/users/siconglu/Mia_WH_Analysis/WHAnalysis/onelepbabymaker/TChiWH_700_1_test.root"]},
{"name":"new (700,100)", "file_name_list":["/home/users/siconglu/Mia_WH_Analysis/WHAnalysis/onelepbabymaker/TChiWH_700_100_test.root"]},
{"name":"new (700,150)", "file_name_list":["/home/users/siconglu/Mia_WH_Analysis/WHAnalysis/onelepbabymaker/TChiWH_700_150_test.root"]},
{"name":"new (600,1)", "file_name_list":["/home/users/siconglu/Mia_WH_Analysis/WHAnalysis/onelepbabymaker/TChiWH_600_1_test.root"]},
{"name":"new (600,100)", "file_name_list":["/home/users/siconglu/Mia_WH_Analysis/WHAnalysis/onelepbabymaker/TChiWH_600_100_test.root"]},
{"name":"new (600,150)", "file_name_list":["/home/users/siconglu/Mia_WH_Analysis/WHAnalysis/onelepbabymaker/TChiWH_600_150_test.root"]},
#{"name":"new 2l top", "file_name_list":["/home/users/siconglu/Mia_WH_Analysis/WHAnalysis/onelepbabymaker/ttbar_di_lep_test.root"]},
#{"name":"new 1l top", "file_name_list":["/home/users/siconglu/Mia_WH_Analysis/WHAnalysis/onelepbabymaker/ttbar_single_lep_test.root"]},
]
import multiprocessing as mp
process_ind = 0
num_cores = 8
processes = []

for MC in tmp_MC_list:
    #plot_comparison(MC, plot_folder_name)
    p = mp.Process(target=plot_comparison, args=(MC, plot_folder_name,))
    processes.append(p)
    process_ind+=1
    if (process_ind+1)%num_cores == 0 or (MC == tmp_MC_list[-1]):            
        [x.start() for x in processes]
        print("Starting %.0f process simultaneously."%len(processes))
        [x.join() for x in processes]
        processes = []



