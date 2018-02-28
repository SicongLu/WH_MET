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

#Get Files
file_location = "../root_file_temp/Mia_20180223/"
sig_name = "TChiWH_350_100"
f = ROOT.TFile(file_location+sig_name+".root")
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
pt_hist = ROOT.TH1F("pt_hist","pt_hist",50,0,600)

form_passMEDbtag_list = []
for i in range(12):
    form_passMEDbtag_list.append(ROOT.TTreeFormula("ak4pfjets_passMEDbtag_%d"%i,\
    "ak4pfjets_passMEDbtag[%d]"%i,t))

cutflow_dict = {"1 good lep":0, "2nd lep veto":0, "track veto":0, "tau veto":0, \
"==2jets":0, "==2 btags":0, "Mbb window":0, "MCT>170GeV":0,"MET>125GeV":0,\
"MT>150GeV":0,"Total":0}

lumi = 36.1
event_num = t.GetEntries()
for i_evt in range(event_num):
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
print(sig_name)
from collections import OrderedDict
cutflow_dict = OrderedDict(sorted(cutflow_dict.items(), key=lambda x: x[1], reverse=True))
for key, value in cutflow_dict.iteritems():
    print(key+"    %.5f" % (value))



