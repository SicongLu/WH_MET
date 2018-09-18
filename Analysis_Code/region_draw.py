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
def draw_histo(file_name, str_condition, MC_name):
    #print(file_name, var_name, str_condition, bin_num, xmin, xmax)
    BTAGWP = 0.5426; #Loose btag working point
    mBTAGWP = 0.8484; #Medium btag working point
    
    f = ROOT.TFile(file_name)
    t = f.Get("t")
    var_name = "dR_bb"
    bin_num = 40
    xmin = 0
    xmax = 3.5
    myhist1 = ROOT.TH1F("myhist1","myhist1",bin_num,xmin,xmax); #Old 2 jet
    myhist2 = ROOT.TH1F("myhist2","myhist2",bin_num,xmin,xmax); #1 jet (ak8 with hbb?
    myhist3 = ROOT.TH1F("myhist3","myhist3",bin_num,xmin,xmax); #The rest of 2 jet orthogonal
    myhist4 = ROOT.TH1F("myhist4","myhist4",bin_num,xmin,xmax); #2 jet not passing the pt but is b-tagged (not from pile-up
    name_list = ["Old 2 jet", "Ext(1 jet hbb)", "Ext(2jet)","Ext(2jet recoverable)"]
    
    #str_condition +="&& ngoodjets == 2"
    #str_condition +="&& ngoodjets30 == 2"
    weight_form = ROOT.TTreeFormula("weight",str_condition,t)
    for i in range(t.GetEntries()):
        if i % 5e3 == 0: print(i)
        #if i>5000: break;
        t.GetEntry(i)
        dR_bb = -999
        weight = weight_form.EvalInstance()
        if weight == 0:
            continue
        #Calculate dR_bb
        m_id = t.genqs_motherid
        v1 = 0
        v2 = 0
        for jet_i in range(len(m_id)):
            if t.genqs_motherid.at(jet_i) == 25 and t.genqs_id.at(jet_i) == -5 and v1 == 0:
                v1 = t.genqs_p4.at(jet_i)
            if t.genqs_motherid.at(jet_i) == 25 and t.genqs_id.at(jet_i) == 5 and v2 == 0:
                v2 = t.genqs_p4.at(jet_i)        
        dR_bb = delta_R(v1,v2)
        #Genenrator info.
        
        p4_list = t.ak4pfjets_p4
        pT_list = [p4.Pt() for p4 in p4_list] 
        pT_list = sorted(pT_list, reverse=True)
        #If it is in 1 jet region
        value = dR_bb
        
        #If in old 2 jet region
        if t.ngoodjets30 == 2:
            myhist1.Fill(value, weight)
            continue;
        elif t.ngoodjets30 > 2:
            continue;
        #If in 1 jet hbb region
        if t.ak8GoodPFJets > 0:
            hbb_flag = False
            for jet_i in range(t.ak8GoodPFJets):
                if t.ak8pfjets_deep_rawdisc_hbb[jet_i]>0.5:
                    hbb_flag = True
                    break;
            if hbb_flag:
                myhist2.Fill(value, weight)
                continue;
        #The rest falls in to 2 jet region
        myhist3.Fill(value, weight)
        #If we can recover this part by using the b-tag
        b_pt_recover_num = 0
        for jet_i in range(t.ngoodjets):
            if t.ak4pfjets_CSV[jet_i]>BTAGWP or t.ak4pfjets_p4[jet_i].Pt()>=30:
                b_pt_recover_num += 1
        if b_pt_recover_num >= 2:
            myhist4.Fill(value, weight)
        
    myhist1.SetDirectory(0);
    myhist2.SetDirectory(0);
    myhist3.SetDirectory(0);
    myhist4.SetDirectory(0);
    
    hist_list = [myhist1, myhist2, myhist3, myhist4] 
    
    f.Close()
    return hist_list, name_list
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
    MC_name = MC["name"]
    tmp_var_name = flatten_var_name(MC_name+"_dR_bb")
    file_name_list = MC["file_name_list"]
    file_name = file_name_list[0]
    file_name = new_location + file_name[file_name.rfind("/")+1:]
    hist_list, name_list = draw_histo(file_name, str_condition, MC_name)
        
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
            "noStack": True,
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
    

#Common set-up 
lumi = 35.9

plot_folder_name = "WH_Comparison_20180618_compare_1jet_2jet/"

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
global new_location
new_location = "/home/users/siconglu/WH_MET/root_file_temp/Sicong_20180605/"
tmp_MC_list = [
{"name":"new (700,1)", "file_name_list":[new_location+"TChiWH_700_1_test.root"]},
{"name":"new (700,100)", "file_name_list":[new_location+"TChiWH_700_100_test.root"]},
{"name":"new (700,150)", "file_name_list":[new_location+"TChiWH_700_150_test.root"]},
{"name":"new (600,1)", "file_name_list":[new_location+"TChiWH_600_1_test.root"]},
{"name":"new (600,100)", "file_name_list":[new_location+"TChiWH_600_100_test.root"]},
{"name":"new (600,150)", "file_name_list":[new_location+"TChiWH_600_150_test.root"]},
#{"name":"new ttbar", "file_name_list":[new_location+"ttbar_di_lep_test.root"]},
#{"name":"new 2l top", "file_name_list":[new_location+"ttbar_di_lep_test.root"]},
#{"name":"new 1l top", "file_name_list":[new_location+"ttbar_single_lep_test.root"]},
]
import multiprocessing as mp
process_ind = 0
num_cores = 8
processes = []

for MC in tmp_MC_list:
    p = mp.Process(target=plot_comparison, args=(MC, plot_folder_name,))
    processes.append(p)
    process_ind+=1
    if (process_ind)%num_cores == 0 or (MC == tmp_MC_list[-1]):            
        [x.start() for x in processes]
        print("Starting %.0f process simultaneously."%len(processes))
        [x.join() for x in processes]
        processes = []



