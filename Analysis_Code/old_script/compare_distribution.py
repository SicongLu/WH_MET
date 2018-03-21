'''
This script intends to make relevant comparison plots.
Some conventions:
'''
import ROOT
import numpy
ROOT.gStyle.SetOptStat(0);
ROOT.gStyle.SetOptTitle(0);
#ROOT.gROOT.SetBatch()
#ROOT.gStyle.SetPaintTextFormat("4.1f");

def retrieve_distribution(file_name):
    '''
    This function get the pt_bb histogram given the file_name and the directory.
    It shall also output the cutflow.
    '''
    #Get Files
    print(file_name)
    f = ROOT.TFile(file_name)
    t = f.Get("t")
    #Only read in relevant variables to increase the speed.
    cut_var_list = ["ngoodleps","nvetoleps","PassTrackVeto","PassTauVeto","ngoodjets",\
    "ngoodbtags","mbb","mct","pfmet","mt_met_lep","ak4pfjets_passMEDbtag",\
    "ak4pfjets_CSV"]
    plot_var_list = ["scale1fb","ak4pfjets_leadMEDbjet_p4"]
    used_var_list = cut_var_list + plot_var_list
    LV_var_list = ["ak4pfjets_p4"]
    #Set the branch status
    t.SetBranchStatus("*",0)
    for used_var in used_var_list:
        t.SetBranchStatus(used_var,1)
    #For Math.LorentzVector we need more branches inside
    LV_suffix_list = [".fCoordinates.fX",".fCoordinates.fY",".fCoordinates.fZ",\
    ".fCoordinates.fT"] #For those that are Math.LorentzVector
    for LV_var in LV_var_list:
        for LV_suffix in LV_suffix_list:       
            t.SetBranchStatus(LV_var+LV_suffix,1)
            
    #Histogram_list
    pt_hist = ROOT.TH1F("pt_hist","pt_hist",20,0,400)
    pt_hist.SetDirectory(0);
    ROOT.TH1.AddDirectory(ROOT.kFALSE); 
    form_passMEDbtag_list = []
    for i in range(12):
        form_passMEDbtag_list.append(ROOT.TTreeFormula("ak4pfjets_passMEDbtag_%d"%i,\
        "ak4pfjets_passMEDbtag[%d]"%i,t))
    
    cutflow_dict = {"1 good lep":0, "2nd lep veto":0, "track veto":0, "tau veto":0, \
    "==2jets":0, "==2 btags":0, "Mbb window":0, "MCT>170GeV":0,"MET>125GeV":0,\
    "MT>150GeV":0,"Total":0}
    
    lumi = 36.1
    event_num = t.GetEntries()
    print("Total: %.0f events..." % (event_num))
    for i_evt in range(event_num):
        if i_evt % 10000 == 0:
            print("Processing %.0f events..." % (i_evt))
        t.GetEntry(i_evt)
        weight = t.scale1fb*lumi
        cutflow_dict["Total"]+=weight
        #1 good lep
        if not(t.ngoodleps == 1):        continue;
        cutflow_dict["1 good lep"]+=weight
        #2nd lep veto
        if not(t.nvetoleps == 1):        continue;
        cutflow_dict["2nd lep veto"]+=weight
        #track veto
        if not(t.PassTrackVeto == 1):        continue;
        cutflow_dict["track veto"]+=weight
        #tau veto
        if not(t.PassTauVeto == 1):        continue;
        cutflow_dict["tau veto"]+=weight
        #==2jets
        if not(t.ngoodjets == 2):        continue;
        cutflow_dict["==2jets"]+=weight
        #==2 btags
        if not(t.ngoodbtags == 2):        continue;
        cutflow_dict["==2 btags"]+=weight
        #Mbb window
        if not(t.mbb >= 90 and t.mbb<=150):        continue;
        cutflow_dict["Mbb window"]+=weight
        #MCT>170GeV
        if not(t.mct >= 170):        continue;
        cutflow_dict["MCT>170GeV"]+=weight
        #MET>125GeV
        if not(t.pfmet >= 125):        continue;
        cutflow_dict["MET>125GeV"]+=weight
        #MT>150GeV
        if not(t.mt_met_lep >= 150):        continue;
        cutflow_dict["MT>150GeV"]+=weight
        #End of cut    
    
        #Reconstruction 
        lead_btag_jet = t.ak4pfjets_leadMEDbjet_p4
        
        jet_list = t.ak4pfjets_p4
        jet_num = len(jet_list)                                                                                         
        for i_jet in range(jet_num):
            if (form_passMEDbtag_list[i_jet].GetNdata() > 0): 
            #It is a temporary solution to a known issue in ROOT, see appendix for details 
                jet_btag_bool = form_passMEDbtag_list[i_jet].EvalInstance()
            if jet_btag_bool == 0:
                continue;
            second_btag_jet = jet_list[i_jet]
        di_bjet = lead_btag_jet+second_btag_jet
        
        pt_hist.Fill(di_bjet.Pt(), weight)    
     
    #Print Efficiency Table
#    print(file_name)
    from collections import OrderedDict
    cutflow_dict = OrderedDict(sorted(cutflow_dict.items(), key=lambda x: x[1], reverse=True))
#    for key, value in cutflow_dict.items():
#        print(key+"    %.5f" % (value))
    return pt_hist, cutflow_dict



#Main function
from create_file_list import get_files
MC_list = get_files()

summary_cutflow_dict = {}
hist_list = []
name_list = []
for MC in MC_list[0:7]:
    MC_name = MC["name"]
    file_name_list = MC["file_name_list"]
    
    sum_hist = ROOT.TH1F("sum_hist","sum_hist",20,0,400)
    sum_hist.SetDirectory(0);  
    ROOT.TH1.AddDirectory(ROOT.kFALSE);
    sum_dict = {}
    for file_name in file_name_list:
        hist, cutflow_dict = retrieve_distribution(file_name)    
        sum_hist.Add( sum_hist, hist, 1.0, 1.0 )
        for key, value in cutflow_dict.items():
            if key in sum_dict.keys():
                sum_dict[key]+=cutflow_dict[key]
            else:
                sum_dict[key]=cutflow_dict[key]
    if "(" in MC_name:
        sum_hist.Scale(50)
        MC_name += " x 50" 
    hist_list.append(sum_hist)
    name_list.append(MC_name)
    summary_cutflow_dict[MC_name] = sum_dict

#Save the Cutflow Table in .csv file
import csv
with open('cutflow_table.csv', 'w') as csvfile:    #create csv file with w mode
    fieldnames = [" "]+name_list          #header names
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)    #set the writer
    writer.writeheader()   
    for key, value in summary_cutflow_dict[name_list[0]].items():
        tmp_row = {" ":key}
        for MC_name in name_list:
            tmp_row[MC_name] = summary_cutflow_dict[MC_name][key]
        writer.writerow(tmp_row) 
#Use dataMCplotMaker
import sys
sys.path.insert(0, '/home/users/siconglu/CMSTAS/software/dataMCplotMaker/')
import dataMCplotMaker

h_data = ROOT.TH1F("","",1,0,1)
d_opts = {
        "poissonErrorsNoZeros": True,
        "lumi": 35.9,
        "energy ": 13,
        "outputName": "plots/test.pdf",
        "yTitleOffset": 0.0,
        "xAxisLabel": "pT_{bb}",
        "yAxisLabel": "Events",
        "xAxisUnit": "GeV",
        "noFill": "GeV",
        "isLinear": True,
        #"legendUp": -0.15,
        #"legendRight": -0.08,
        #"legendTaller": 0.15,
        "outOfFrame": True,
        "type": "Internal",
        #"noGrass": True,
        "darkColorLines": True,
        "makeTable": True,
        "makeJSON": True
        #"flagLocation": "0.5,0.7,0.15", # add a US flag because 'merica
        }
color_list = [ROOT.kOrange, ROOT.kSpring, ROOT.kTeal,ROOT.kAzure, ROOT.kViolet, ROOT.kPink, ROOT.kBlack]
dataMCplotMaker.dataMCplot(h_data, bgs=hist_list, titles=name_list, title="", colors=color_list[0:len(name_list)], opts=d_opts)



